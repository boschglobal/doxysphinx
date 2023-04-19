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
import logging
from pathlib import Path
from typing import Iterable, List, Optional, Tuple, Type

from mpire import WorkerPool

from doxysphinx.html_parser import DoxygenHtmlParser, HtmlParser
from doxysphinx.resources import DoxygenResourceProvider, ResourceProvider
from doxysphinx.sphinx import DirectoryMapper, SphinxHtmlBuilderDirectoryMapper
from doxysphinx.utils.files import hash_blake2b
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
        parallel=True,
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
        self._parallel = parallel

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
        parser = self._parser_type(doxygen_html_dir)
        writer = self._writer_type(doxygen_html_dir)
        task_args: Tuple[HtmlParser, Writer] = (parser, writer)

        files_with_hashes = list(self._get_doxy_htmls_to_process_with_hashes(doxygen_html_dir))

        if self._parallel:
            with WorkerPool() as pool:
                pool.set_shared_objects(task_args)
                result = pool.map(self._run, files_with_hashes)
                return result
        else:
            return [self._run((parser, writer), f[0], f[1]) for f in files_with_hashes]

    def _get_doxy_htmls_to_process_with_hashes(self, doxygen_html_dir: Path) -> Iterable[Tuple[Path, str]]:
        """Get all doxygen html files to process with their hashes (blake2b).

        The hashes are used to implement incremental behavior. So only files which aren't the same are
        processed.
        """
        for html_file in doxygen_html_dir.glob("*.html"):
            rst_file = html_file.with_suffix(".rst")

            hash_from_html = hash_blake2b(html_file)

            if not rst_file.exists():
                yield html_file, hash_from_html
                continue

            hash_from_rst = self._get_html_hash_from_rst(rst_file)

            if hash_from_rst == hash_from_html:
                self._logger.debug(f"skipping {html_file} as the rst was created before.")
                continue

            yield html_file, hash_from_html

    def _get_html_hash_from_rst(self, rst_file: Path) -> Optional[str]:
        if not rst_file.exists():
            return None

        with rst_file.open(encoding="utf-8") as file:
            rst_content = [next(file) for x in range(1)]

        if not rst_content:
            return None

        if not rst_content[0].startswith(".. meta::"):
            return None

        # take everything from the last ":" onwards and return it (=the hash)
        hash_from_rst = rst_content[0].split(":")[-1].rstrip()
        return hash_from_rst

    def _run(self, task_args: Tuple[HtmlParser, Writer], html_file: Path, html_hash: str) -> Path:
        parser, writer = task_args

        # parse the doxygen html file
        parse_result = parser.parse(html_file)

        rst_file = html_file.with_suffix(".rst")

        # write the corresponding rst file
        result = writer.write(parse_result, rst_file, html_hash)

        return result


class Cleaner:
    """The cleaner cleans files created and copied by the builder."""

    _logger = logging.getLogger(__name__)

    def __init__(
        self,
        sphinx_source_dir: Path,
        sphinx_output_dir: Path,
        dir_mapper_type: Type[DirectoryMapper] = SphinxHtmlBuilderDirectoryMapper,
        resource_provider_type: Type[ResourceProvider] = DoxygenResourceProvider,
        parallel: bool = True,
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
        self._parallel = parallel

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
        files = list(doxygen_html_dir.glob("*.html"))

        if self._parallel:
            with WorkerPool() as pool:
                pool.set_shared_objects(self._logger)
                return pool.map(self._delete_corresponding_file, files)
        else:
            return [result for file in files if (result := self._delete_corresponding_file(self._logger, file))]

    @staticmethod
    def _delete_corresponding_file(logger: logging.Logger, html_file: Path) -> Optional[Path]:
        target_rst_path = html_file.with_suffix(".rst")
        if target_rst_path.exists():
            target_rst_path.unlink()
            logger.debug(f"deleted {target_rst_path}")
            return target_rst_path
        return None
