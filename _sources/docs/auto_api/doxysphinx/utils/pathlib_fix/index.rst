doxysphinx.utils.pathlib_fix
============================

.. py:module:: doxysphinx.utils.pathlib_fix

.. autoapi-nested-parse::

   The pathlib_fix module contains several pathlib fixes.



Functions
---------

.. autoapisummary::

   doxysphinx.utils.pathlib_fix.path_resolve
   doxysphinx.utils.pathlib_fix.path_is_relative_to


Module Contents
---------------

.. py:function:: path_resolve(path: pathlib.Path) -> pathlib.Path

   Fix/Workaround for bug https://bugs.python.org/issue38671.

   On Windows resolve will not return correct absolute paths for non-existing files
   (only for existing ones). This got fixed in python 3.10, however as we need to
   support older versions....


.. py:function:: path_is_relative_to(path: pathlib.Path, base: pathlib.Path) -> bool

   Fix/Workaround for strange behavior in python 3.8.

   The issue is that Path.is_relative_to complains about PosixPath not having such an attribute in a
   foreign project.


