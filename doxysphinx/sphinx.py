# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""The sphinx module contains classes that are tied to sphinx or resemble sphinx logic."""

from pathlib import Path
from typing import Protocol

# noinspection PyMethodMayBeStatic,PyUnusedLocal
from doxysphinx.utils.pathlib_fix import path_resolve


class DirectoryMapper(Protocol):
    """
    Mapper that will calculate the output file path for an input file.

    In docs-as-code tooling (e.g. sphinx) often files from a source dir
    structure are processed and written to result files in a target dir structure.

    The make this mapping an implementation detail this protocol exists.
    It should be implemented for any special handling in mapping files.
    """

    def __init__(self, sphinx_source_dir: Path, sphinx_output_dir: Path):
        """
        Protocol for a directory mapper constructor.

        :param sphinx_source_dir: the sphinx source directory
        :param sphinx_output_dir: the sphinx output directoryS
        """

    def map(self, path: Path) -> Path:
        """Calculate the path in output for a given path in input."""
        return Path()


class SphinxHtmlBuilderDirectoryMapper:
    """
    Mapper that will calculate the output file path for an input file.

    This is based on the logic that the sphinx html builder would use.
    """

    def __init__(self, sphinx_source_dir: Path, sphinx_output_dir: Path):
        """
        Create a sphinx html builder directory mapper.

        This mapper resembles the behavior of the sphinx html build considering path
        handling and copying to output.

        :param sphinx_source_dir: the sphinx source directory
        :param sphinx_output_dir: the sphinx output directoryS
        """
        self.source = sphinx_source_dir
        self.output = sphinx_output_dir

    def map(self, path: Path) -> Path:
        """Calculate the path in output for a given path in input."""
        if path.is_absolute():
            return self._map_absolute(path)
        else:
            return self._map_relative(path)

    def _map_absolute(self, path: Path) -> Path:
        relative_source_path = path.relative_to(path_resolve(self.source))
        output_path = path_resolve(self.output) / relative_source_path
        return output_path

    def _map_relative(self, path: Path) -> Path:
        relative_source_path = path_resolve(path).relative_to(path_resolve(self.source))
        output_path = path_resolve(self.output) / relative_source_path
        return output_path.relative_to(Path.cwd())
