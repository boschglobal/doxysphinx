doxysphinx.utils.files
======================

.. py:module:: doxysphinx.utils.files

.. autoapi-nested-parse::

   The files module contains several file related helper functions.



Functions
---------

.. autoapisummary::

   doxysphinx.utils.files.write_file
   doxysphinx.utils.files.replace_in_file
   doxysphinx.utils.files.multi_replace_in_file
   doxysphinx.utils.files.multi_glob
   doxysphinx.utils.files.copy_if_different
   doxysphinx.utils.files.stringify_paths
   doxysphinx.utils.files.hash_blake2b


Module Contents
---------------

.. py:function:: write_file(file: pathlib.Path, data: Iterable[str], separator: Optional[str] = None)

   Write an array of lines to a file in one call.

   :param file: The path to the file.
   :param data: An array of lines to write to the file.
   :param separator: The line separator. Defaults to os.linesep = autodetect for current os.
       If you want to force a unix "lf" file use '\n',
       if you want to force a windows "crlf" file use '\r\n'., defaults to None


.. py:function:: replace_in_file(file: pathlib.Path, search: str, replacement: str)

   Replace a text in a file.

   :param file: The file to do the replacement in.
   :param search: The text to search inside the file.
   :param replacement: The replacement text.


.. py:function:: multi_replace_in_file(file: pathlib.Path, *search_replace_pair: Tuple[str, str])

   Replace text inside a file. Supports multiple replacements.

   :param file: The file to do the replacement in.
   :param search_replace_pair: an argument list of search and replacement text pairs.


.. py:function:: multi_glob(directory: pathlib.Path, *patterns: str) -> List[pathlib.Path]

   Evaluate multiple glob patterns at once.

   :param directory: The source directory (where to evaluate the glob pattern)
   :param patterns: The glob patterns as list or multi-arguments
   :returns: The list of found files/directories


.. py:function:: copy_if_different(source_dir: pathlib.Path, target_dir: pathlib.Path, *patterns: str, ignore_files: Optional[List[pathlib.Path]] = None) -> List[pathlib.Path]

    Copy files with given glob patterns from source_dir to target_dir but only if the files are different.

   :param source_dir: The source directory of the files to copy
   :param target_dir: The target directory where the files are copied to
   :param patterns: glob patterns for the source files
   :return: a list of all files that were copied (target files)


.. py:function:: stringify_paths(paths: Iterable[pathlib.Path]) -> str

   Convert a list of paths to a bulleted string where each path is on a new line.


.. py:function:: hash_blake2b(file: pathlib.Path, chunk_size: int = 65536) -> str

   Fast file hash based on blake2b hash algorithm.

   :param file: Path to a file to calculate the hash for
   :param chunk_size: The size of the chunks that are read from the file. Use this if you really need to
       optimize for performance for your special use case. Note that the default (64k) turned out the fastest
       in some very naive adhoc tests... so there may be room for improvement here.



