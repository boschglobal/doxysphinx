# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
#  - Aniket Salve, Robert Bosch GmbH
# =====================================================================================

"""
The process module contains the :class:`Builder` and :class:`Cleaner` classes.

These represent the main functionality of doxysphinx.
"""
import hashlib
import logging
from pathlib import Path
from typing import List, Type

from doxysphinx.html_parser import DoxygenHtmlParser, HtmlParser
from doxysphinx.resources import DoxygenResourceProvider, ResourceProvider
from doxysphinx.sphinx import DirectoryMapper, SphinxHtmlBuilderDirectoryMapper
from doxysphinx.writer import RstWriter, Writer


class Builder:
    """
    The Builder builds target docs-as-code files out of an existing html documentation.

    For each an every html file a rst file is created that imports the html content
    with raw directives. The html resources (stylesheets, images etc.) are also processed
    and copied to the correct place in the sphinx output directory.
    When sphinx then (later - not part of doxysphinx) processes the rst files they will
    resemble the original filenames in the sphinx output directory, thereby keeping
    and internal links intact.
    """

    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        sphinx_source_dir: Path,
        sphinx_output_dir: Path,
        dir_mapper_type: Type[DirectoryMapper] = SphinxHtmlBuilderDirectoryMapper,
        resource_provider_type: Type[ResourceProvider] = DoxygenResourceProvider,
        parser_type: Type[HtmlParser] = DoxygenHtmlParser,
        writer_type: Type[Writer] = RstWriter,
        force_recreation: bool = False,
    ):
        """
        Create a Builder that builds rsts for doxygen html files.

        :param sphinx_source_dir: The sphinx source directory where the rst files are
                                  located (most of the time something like "docs")
        :param sphinx_output_dir: The sphinx output directory where the final
                                  documentation is located.
        :param dir_mapper_type: The type of directory mapper to use.
        :param resource_provider_type: The resource provider to use.
        :param parser_type: The html parser to use.
        :param writer_type: The writer type to use.
        :param force_recreation: whether to force the recreation of rst files

        """
        self._dir_mapper = dir_mapper_type(sphinx_source_dir, sphinx_output_dir)
        self._resource_provider = resource_provider_type(self._dir_mapper)

        # these will be used later lazily
        self._parser_type = parser_type
        self._writer_type = writer_type
        self._force_recreation = force_recreation

    def build(self, doxygen_html_dir: Path):
        """
        Generate a rst file for each doxygen html file.

        Also copies necessary resources.

        :param doxygen_html_dir: The html output directory of doxygen where the
                                 generated documentation is.
        """
        copied_resources = self._resource_provider.provide_resources(doxygen_html_dir)
        self._logger.info(
            f"copied {len(copied_resources)} resource-files " f"to {self._dir_mapper.map(doxygen_html_dir)}"
        )

        created_rsts = self._build(doxygen_html_dir)
        self._logger.info(f"created {len(created_rsts)} rst-files in {doxygen_html_dir}")

    def _build(self, doxygen_html_dir: Path) -> List[Path]:
        result_list: List[Path] = []
        parser = self._parser_type(doxygen_html_dir)
        writer = self._writer_type(doxygen_html_dir)

        for html_file in doxygen_html_dir.glob("*.html"):
            parse_result = parser.parse(html_file)

            # for now, we just write the rst parallel to the html file
            rst_file = html_file.with_suffix(".rst")

            # get hash of the html file
            html_text = html_file.read_text()
            html_hash = hashlib.blake2b(html_text.encode("utf-8")).hexdigest()

            # if the rst file is either not existing or the html file is not changed...
            if self._should_build_rst(rst_file, html_hash):
                result_list.append(writer.write(parse_result, rst_file, html_hash))

        return result_list

    def _should_build_rst(self, rst_file: Path, html_hash: str) -> bool:

        # always build if force mode is on
        if self._force_recreation:
            return True

        # always build if rst file is not existing
        if not rst_file.exists():
            return True

        # read the line first line of RST file
        with open(rst_file, encoding="utf-8") as myfile:
            rst_content = [next(myfile) for x in range(1)]

        # return false if meta data is not found in first line
        if not rst_content[0].startswith(".. meta::"):
            return False

        # return true if hash matches with the meta data
        hash_from_rst = rst_content[0].split(":")[-1].rstrip()
        if hash_from_rst != html_hash:
            return True

        return False


class Cleaner:
    """The cleaner cleans files created and copied by the builder."""

    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        sphinx_source_dir: Path,
        sphinx_output_dir: Path,
        dir_mapper_type: Type[DirectoryMapper] = SphinxHtmlBuilderDirectoryMapper,
        resource_provider_type: Type[ResourceProvider] = DoxygenResourceProvider,
    ):
        """
        Create a Cleaner that will cleanup things that the :class:`Builder` created.

        :param sphinx_source_dir: The sphinx source directory where the rst files are
                                  located (most of the time something like "docs")
        :param sphinx_output_dir: The sphinx output directory where the final
                                  documentation is located.
        :param dir_mapper_type: The type of directory mapper to use.
        :param resource_provider_type: The resource provider to use.
        :param parser_type: The html parser to use.
        :param writer_type: The writer type to use.

        """
        self._dir_mapper = dir_mapper_type(sphinx_source_dir, sphinx_output_dir)
        self._resource_provider = resource_provider_type(self._dir_mapper)

    def cleanup(self, doxygen_html_dir: Path):
        """
        Clean up files that were generated by the build method.

        :param doxygen_html_dir: The html output directory of doxygen where the
            generated documentation is.
        """
        resource_target_dir = self._dir_mapper.map(doxygen_html_dir)
        deleted_resources = self._resource_provider.cleanup_resources(resource_target_dir)
        self._logger.info(f"deleted {len(deleted_resources)} resource-files from {resource_target_dir}")

        deleted_rsts = self._cleanup(doxygen_html_dir)
        self._logger.info(f"deleted {len(deleted_rsts)} rst-files from {doxygen_html_dir}")

    def _cleanup(self, doxygen_html_dir: Path) -> List[Path]:
        result_list: List[Path] = []
        for file_path in doxygen_html_dir.glob("*.html"):
            target_rst_path = file_path.with_suffix(".rst")
            if target_rst_path.exists():
                target_rst_path.unlink()
                result_list.append(target_rst_path)
                self._logger.debug(f"deleted {target_rst_path}")
        return result_list
