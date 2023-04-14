# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""
The resources module contains classes will do resource provisioning and patching.

Resources are stylesheets, images, javascripts etc. that contemplate the html files.
"""

import hashlib
import logging
import pkgutil
from pathlib import Path
from typing import Any, Callable, List, Optional, Protocol, Union

import sass

from doxysphinx.sphinx import DirectoryMapper

# noinspection PyMethodMayBeStatic,PyUnusedLocal
from doxysphinx.utils.exceptions import ApplicationError
from doxysphinx.utils.files import copy_if_different, multi_glob, stringify_paths


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

    def _load_custom_styles(self) -> str:
        data: Union[bytes, None] = pkgutil.get_data(__name__, "resources/custom.scss")
        if data:
            return "\n" + data.decode("utf-8") + "\n"
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

        # copy file that are different in target, except for css files that we post process later (the
        # difference check would fail for them anyway)
        doxygen_css = resource_root / "doxygen.css"
        doxygen_awesome_css = resource_root / "doxygen-awesome.css"
        css_files_for_postprocessing = [doxygen_css, doxygen_awesome_css]
        copied_files = copy_if_different(
            resource_root, target, *self._provisioning_glob_pattern, ignore_files=css_files_for_postprocessing
        )

        self._logger.debug(f"copied files:\n{stringify_paths(copied_files)}")

        # postprocessing (patching + sass)
        # ... for doxygen.css
        written_doxygen_css = self._css_scoper.scope(
            stylesheet=doxygen_css,
            target=target / doxygen_css.name,
            additional_css_rules=self._custom_styles,
            content_patch_callback=lambda s: str.replace(s, "code.JavaDocCode\n", "code.JavaDocCode {\n"),
        )
        if written_doxygen_css:
            copied_files.append(written_doxygen_css)
        # ... for doxygen_awesome.css if existing
        if doxygen_awesome_css.exists():
            written_doxygen_awesome_css = self._css_scoper.scope(
                stylesheet=doxygen_awesome_css,
                target=target / doxygen_awesome_css.name,
                content_patch_callback=lambda s: str.replace(s, "invert()", '#{"invert()"}'),
            )
            if written_doxygen_awesome_css:
                copied_files.append(written_doxygen_awesome_css)

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


class CssScoper:
    """Scopes css-stylesheets to a special selector.

    This is done with the help of libsass (as the sass-syntax extends css with nesting).

    Our original problem was that the doxygen stylesheet and the sphinx theme stylesheets collide in some
    ways (e.g. global styles like heading-styles etc...). We therefore needed to have a mechanism to apply
    doxygen stylesheets only to doxygen content (not to the outer sphinx theme shell). We do this via sass,
    because sass is css compatible but adds some nice features to it. You can for example nest styles.
    We use that here to define an outer class and nest the whole doxygen stylesheet below it in a temporary
    sass stylesheet which then gets compiled back to css. With this
    we kill 2 birds with one stone:
    * all doxygen rules are now scoped so they are not applied to the sphinx bits shell anymore....
    * all doxygen rules now are more specialized than any of the outer sphinx style rules (they will win in browser).

    In the end that means that sphinx styles are applied to sphinx bits and doxygen styles are applied to
    doxygen bits. We still need to fix some minor issues with a custom stylesheet (which we also apply here).
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
        target: Path,
        additional_css_rules: Optional[str] = None,
        content_patch_callback: Optional[Callable[[str], str]] = None,
    ) -> Optional[Path]:
        """Scope a stylesheet to given selector.

        The process is as follows: The original stylesheet is read, processed, hashed and compiled to the
        target. If a target already exists and the hash is identical nothing is compiled and written.

        :param stylesheet: The path to a stylesheet to scope.
        :param: target: The path to a stylesheet where the results are written to.
        :param additional_css_rules: Additional css rules to inject.
        :param scss_patch_callback: A callback that will be called on the original file.
               Note: we had a bug in doxygen.css and a sass compatibility fix for doxygen-awesome that made
               this mechanism necessary. With one of the recent doxygen versions the doxygen.css bug was fixed
               however we still keep it here some time.
        :return: The path to the written stylesheet (should be identical to stylesheet).
        """
        if stylesheet == target:
            raise ApplicationError(f"source ({stylesheet}) and target ({target}) stylesheets cannot be identical.")

        # load stylesheet and apply patches
        css_content = stylesheet.read_text()

        if content_patch_callback:
            css_content = content_patch_callback(css_content)

        # create .scss (sass) content scoped to the selector
        content = f"{self._selector} {{\n{css_content}\n}}\n"  # here we scope the content to a given css selector

        if additional_css_rules:
            content += additional_css_rules

        new_hash_digest = hashlib.blake2b(content.encode("utf-8")).hexdigest()

        old_hash_digest = self._read_hash_digest(target)
        if new_hash_digest == old_hash_digest:
            return None

        # add hash digest to content
        content = (
            f"/* {new_hash_digest} <- doxysphinx hash digest for the original input css that leads"
            f"to the css below */\n{content}"
        )

        # compile the scss to a css
        compiled_css: Any = sass.compile(
            string=content,
            output_style="expanded",
            indented=False,
            include_paths=[str(stylesheet.parent)],
        )

        # the sass compiler does also scope the html element (where typically css variables are
        # stored). We need to remove that scoping again because it will only work if it's in global scope.
        compiled_css = compiled_css.replace(f"{self._selector} html {{", "html {")

        # write stylesheet
        target.write_text(compiled_css)

        self._logger.debug(
            f"scoped original stylesheet '{stylesheet}' to selector '{self._selector}' in target '{target}'."
        )
        return target

    @staticmethod
    def _read_hash_digest(file: Path) -> str:
        if not file.exists():
            return ""

        digest_line: str
        with open(file, mode="r", encoding="utf") as f:
            digest_line = f.readline()
            # sometimes sass renders an @charset css directive which has to be on the first line (by css spec)
            # so in that case our hash digest is on the second line and we need to adapt to that...
            if digest_line.startswith("@charset"):
                digest_line = f.readline()

        if not digest_line.startswith("/* "):
            return ""

        digest = digest_line[3:].split(" <- ")[0]
        return digest

    @staticmethod
    def _move(original: Path, new: Path):
        if new.exists():
            new.unlink()
        original.rename(new)
