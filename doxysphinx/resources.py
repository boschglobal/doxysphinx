# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""
The resources module contains classes will do resource provisioning and patching.

Resources are stylesheets, images, javascripts etc. that contemplate the html files.
"""

import logging
import pkgutil
from pathlib import Path
from subprocess import run  # nosec: B404
from typing import Callable, List, Optional, Protocol, Union

from doxysphinx.sphinx import DirectoryMapper

# noinspection PyMethodMayBeStatic,PyUnusedLocal
from doxysphinx.utils.exceptions import ApplicationError, PrerequisiteNotMetError
from doxysphinx.utils.files import (
    copy_if_different,
    multi_glob,
    replace_in_file,
    stringify_paths,
    write_file,
)
from doxysphinx.utils.iterators import apply_if_first


class ResourceProvider(Protocol):
    """A resource provider copies/adapts necessary resources (images, stylesheets, etc.) to output."""

    def __init__(self, directory_mapper: DirectoryMapper):
        """
        Protocol constructor.

        :param directory_mapper: the directory mapper to use.
        """
        pass

    def provide_resources(self, resource_root: Path) -> List[Path]:
        """
        Provide necessary resources to sphinx output directory.

        Can also do postprocessing etc.

        :param resource_root: the root resource input directory (e.g. where the html
            files are located)
        :return: A list of resources (their target paths) that were copied/provided.
            Note that in case of some caching (copy if newer) mechanisms this might
            return only parts of the resources.
        """
        return []

    def cleanup_resources(self, resource_root: Path) -> List[Path]:
        """
        Clean up provided resources that were copied by :meth:`provide_resources`.

        :param resource_root: the root resource input directory (e.g. where the html
            files are located)
        :return: A list of resources (their target paths) that were cleaned up/removed.
        """
        return []


class DoxygenResourceProvider:
    """
    Resource provider that will copy/adapt doxygen html resources to output.

    Resource are e.g. stylesheets, images, javascript files etc.
    """

    _logger = logging.getLogger(__name__)

    # constant-ish patterns
    _provisioning_glob_pattern = [
        "*.css",
        "*.js",
        "*.map",
        "*.md5",
        "*.svg",
        "*.png",
        "search/*.*",
    ]
    _cleanup_glob_pattern = _provisioning_glob_pattern + ["*.scss"]

    def __init__(self, directory_mapper: DirectoryMapper):
        """
        Create a doxygen resource provider.

        :param directory_mapper: a directory mapper to use.
        """
        self._dir_mapper = directory_mapper
        self._css_scoper = CssScoper(".doxygen-content")
        self._custom_styles = self._load_custom_styles()

    def _load_custom_styles(self) -> List[str]:
        data: Union[bytes, None] = pkgutil.get_data(__name__, "resources/custom.scss")
        if data:
            return data.decode("utf-8").split("\n")
        else:
            self._logger.critical("could not read custom styles out of package. Exiting.... sorry! :-(")
            exit()

    def provide_resources(self, resource_root: Path) -> List[Path]:
        """
        Copy doxygen html resource files (see GLOB_PATTERN below) to sphinx output.

        The content in the raw html directives can then access these directly.

        :type resource_root: the root of the resources (= usually the same folder where
            the html file are located).
        """
        target = self._dir_mapper.map(resource_root)
        target.mkdir(parents=True, exist_ok=True)

        copied_files = copy_if_different(resource_root, target, *self._provisioning_glob_pattern)

        self._logger.debug(f"copied files:\n{stringify_paths(copied_files)}")

        self._post_process(copied_files)

        return copied_files

    def cleanup_resources(self, resource_root: Path) -> List[Path]:
        """Clean up any provisioned resources that were copied to sphinx output."""
        target = self._dir_mapper.map(resource_root)
        target.mkdir(parents=True, exist_ok=True)

        cleanup_sources = multi_glob(resource_root, *self._cleanup_glob_pattern)
        files_deleted: List[Path] = []
        for source_file in cleanup_sources:
            target_file = target / source_file.relative_to(resource_root)
            if target_file.exists():
                target_file.unlink()
                self._logger.debug(f"deleted {target_file}")
                files_deleted.append(target_file)

        return files_deleted

    def _post_process(self, copied_files: List[Path]):
        # stylesheet scoping
        apply_if_first(
            copied_files,
            lambda p: p.name == "doxygen.css",
            self._patch_doxygen_stylesheet,
        )
        apply_if_first(
            copied_files,
            lambda p: p.name == "doxygen-awesome.css",
            self._patch_doxygen_awesome_stylesheet,
        )

    def _patch_doxygen_stylesheet(self, doxygen_css_file: Path):
        self._css_scoper.scope(
            doxygen_css_file,
            self._custom_styles,
            scss_patch_callback=lambda file: replace_in_file(file, "code.JavaDocCode\n", "code.JavaDocCode {\n"),
        )

    def _patch_doxygen_awesome_stylesheet(self, doxygen_awesome_css_file: Path):
        self._css_scoper.scope(
            doxygen_awesome_css_file,
            scss_patch_callback=lambda file: replace_in_file(file, "invert()", '#{"invert()"}'),
        )


class CssScoper:
    """Scopes css-stylesheets to a special selector.

    This is done with the help of dartsass (a sass processor).
    """

    _logger = logging.getLogger(__name__)

    def __init__(self, css_selector: str):
        """
        Create a new CssScoper.

        :param css_selector: The selector where the stylesheets should be scoped under.
        """
        self._selector = css_selector

    def scope(
        self,
        stylesheet: Path,
        additional_css_rules: Optional[List[str]] = None,
        scss_patch_callback: Optional[Callable[[Path], None]] = None,
    ) -> Path:
        """
        Scopes a stylesheet to given selector.

        The process is as follows: The original stylesheet will be moved to .original.scss.
        Then an scss file (same name like stylesheet) that will import that .original.scss
        file will be created. This will be compiled to the same filename as the original
        stylesheet with the help of dartsass.

        :param stylesheet: The stylesheet to scope.
        :param additional_css_rules: Additional css rules to inject.
        :param scss_patch_callback: A callback that will be called on the original file
        :return: The path to the written stylesheet (should be identical to stylesheet).
        """
        # move original stylesheet to .original.scss
        original = stylesheet.with_suffix(".original.scss")
        self._move(stylesheet, original)

        # execute patch callback if any
        if scss_patch_callback:
            scss_patch_callback(original)

        # create .scss (sass) file that will import the .original.scss but scoped to
        # the selector
        content = [f"{self._selector} {{", f'   @import "{original.name}";', "}", ""]

        if additional_css_rules:  # add additional styles if any
            content.extend(additional_css_rules)

        sass_stylesheet = stylesheet.with_suffix(".scss")
        write_file(sass_stylesheet, content)

        # compile scoped scss to css (thereby retaining original file)
        self._call_sass(sass_stylesheet, stylesheet)

        # remove scoping from html element (if any) where typically variables are
        # stored, because this will only work globally.
        replace_in_file(stylesheet, f"{self._selector} html {{", "html {")

        self._logger.debug(f"scoped stylesheet '{stylesheet}' to selector '{self._selector}'.")
        return stylesheet

    @staticmethod
    def _move(original: Path, new: Path):
        if new.exists():
            new.unlink()
        original.rename(new)

    @staticmethod
    def _call_sass(sass_file: Path, output_css_file: Path):
        try:
            result = run(["sass", sass_file, output_css_file])  # nosec: B607, B603
            result.check_returncode()

            if result.stderr:
                message = (
                    "Sass Compiler had errors "
                    f"(call: sass {sass_file}"  # type: ignore [str-bytes-safe]
                    f"{output_css_file}): \n{result.stderr}"
                )

                raise ApplicationError(message)
        except FileNotFoundError:
            raise PrerequisiteNotMetError(
                "The dart-sass-compiler 'sass' wasn't found. This is a prerequisite "
                "for us to fix stylesheet issues when integrating doxygen html "
                "documentation with sphinx. Please install it either by using the "
                "official guide (https://sass-lang.com/install) or by downloading the "
                "binary directly and putting it on your $PATH "
                "(https://github.com/sass/dart-sass/releases)."
            )
