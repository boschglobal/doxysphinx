# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""The files module contains several file related helper functions."""

import os
import shutil
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

from .exceptions import ValidationError


def write_file(file: Path, data: Iterable[str], separator: Optional[str] = None):
    r"""
    Write an array of lines to a file in one call.

    :param file: The path to the file.
    :param data: An array of lines to write to the file.
    :param separator: The line separator. Defaults to os.linesep = autodetect for current os.
        If you want to force a unix "lf" file use '\n',
        if you want to force a windows "crlf" file use '\r\n'., defaults to None
    """
    if not separator:
        separator = os.linesep

    with open(file, "wb") as file_handler:
        for item in data:
            file_handler.write(f"{item}{separator}".encode("utf-8"))


def replace_in_file(file: Path, search: str, replacement: str):
    """
    Replace a text in a file.

    :param file: The file to do the replacement in.
    :param search: The text to search inside the file.
    :param replacement: The replacement text.
    """
    multi_replace_in_file(file, (search, replacement))


def multi_replace_in_file(file: Path, *search_replace_pair: Tuple[str, str]):
    """
    Replace text inside a file. Supports multiple replacements.

    :param file: The file to do the replacement in.
    :param search_replace_pair: an argument list of search and replacement text pairs.
    """
    content = file.read_text(encoding="utf-8")
    for search, replacement in search_replace_pair:
        content = content.replace(search, replacement)
    file.write_text(content, encoding="utf-8")


def multi_glob(directory: Path, *patterns: str) -> List[Path]:
    """
    Evaluate multiple glob patterns at once.

    :param directory: The source directory (where to evaluate the glob pattern)
    :param patterns: The glob patterns as list or multi-arguments
    :returns: The list of found files/directories
    """
    return [path for p in patterns for path in directory.glob(p)]


class _FileByNameAndSize:
    """
    Implementation Detail.

    A Path Wrapper that implements its identity via name and size only
    (for Set functions like difference).
    """

    def __init__(self, path: Path):
        self.name = path.name
        self.size = path.stat().st_size
        self.path = path

    def __hash__(self) -> int:
        return hash((self.name, self.size))

    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()

    def __repr__(self) -> str:
        return f"{self.path.__repr__()} [{self.size}]"


def copy_if_different(source_dir: Path, target_dir: Path, *patterns: str) -> List[Path]:
    """
     Copy files with given glob patterns from source_dir to target_dir but only if the files are different.

    :param source_dir: The source directory of the files to copy
    :param target_dir: The target directory where the files are copied to
    :param patterns: glob patterns for the source files
    :return: a list of all files that were copied (target files)
    """
    if not source_dir.is_dir():
        raise ValidationError(f"source_dir ({source_dir}) has to be a directory.")
    if not target_dir.is_dir():
        raise ValidationError(f"target_dir ({target_dir}) has to be a directory.")

    target_dir.mkdir(parents=True, exist_ok=True)

    # for each source file try to find a target (an existing file)
    source_files = multi_glob(source_dir, *patterns)
    target_files: List[Path] = [t for t in [target_dir / f.relative_to(source_dir) for f in source_files] if t.exists()]

    # create the set difference to find the files that need to be copied
    source_files_set = {_FileByNameAndSize(s) for s in source_files}
    target_files_set = {_FileByNameAndSize(t) for t in target_files}
    files_to_copy = source_files_set - target_files_set

    result: List[Path] = []
    for file in files_to_copy:
        source_file = file.path
        target_file = target_dir / source_file.relative_to(source_dir)
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_file, target_file)
        result.append(target_file)

    return result


def stringify_paths(paths: Iterable[Path]) -> str:
    """Convert a list of paths to a bulleted string where each path is on a new line."""
    path_list = [str(p) for p in paths]
    if not path_list:
        return "[]"
    return "- " + "\n- ".join(path_list)
