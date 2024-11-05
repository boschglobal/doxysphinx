doxysphinx.doxygen
==================

.. py:module:: doxysphinx.doxygen

.. autoapi-nested-parse::

   The doxygen module contains classes and functions specific to doxygen.



Attributes
----------

.. autoapisummary::

   doxysphinx.doxygen.ConfigDict


Classes
-------

.. autoapisummary::

   doxysphinx.doxygen.DoxyOutput
   doxysphinx.doxygen.DoxygenSettingsValidator
   doxysphinx.doxygen.DoxygenOutputPathValidator


Functions
---------

.. autoapisummary::

   doxysphinx.doxygen.read_doxyconfig
   doxysphinx.doxygen.read_js_data_file


Module Contents
---------------

.. py:data:: ConfigDict

.. py:class:: DoxyOutput

   Class to summarize the strings of the console output and error streams.


   .. py:attribute:: out
      :type:  str


   .. py:attribute:: err
      :type:  str


.. py:function:: read_doxyconfig(doxyfile: pathlib.Path, doxygen_exe: str, doxygen_cwd: pathlib.Path) -> ConfigDict

   Read doxyconfig and get full doxygen configuration (also with default values).

   Supplement the doxygen configuration file with the default doxygen configuration and return the final
   key value pairs as a dict.

   :param doxyfile: the doxygen configuration file to read
   :param doxygen_exe: in case one wants to execute doxygen from another directory.
   :return: a dict representing all key-value pairs defined in the final configuration
            (including warnings from the console output). The value can either be a single value or a list.


.. py:class:: DoxygenSettingsValidator

   Validate doxygen settings for compatibility with doxysphinx.

   Doxysphinx requires some settings to be present/set in a specific way.


   .. py:attribute:: mandatory_settings

      A dictionary containing mandatory settings for the doxygen config.
      The values of OUTPUT_DIRECTORY and GENERATE_TAGFILE will be set after instantiation and validation of the filepaths.


   .. py:attribute:: optional_settings

      A dictionary containing further optional settings for the doxygen config.


   .. py:attribute:: validation_errors
      :type:  List[str]
      :value: []


      List of the validation errors including the doxyflag with its used and the correct value.


   .. py:attribute:: absolute_out
      :type:  pathlib.Path

      Absolute path of the output directory.


   .. py:attribute:: validation_msg
      :value: ''


      Validation errors merged in one string.


   .. py:method:: validate(config: ConfigDict, sphinx_source_dir: pathlib.Path, doxygen_cwd: pathlib.Path) -> bool

      Validate the doxygen configuration regarding the output directory, mandatory and optional settings.

      :param config: the imported doxyfile.
      :param sphinx_source_dir: the sphinx directory (necessary for output directory validation).
      :param doxygen_cwd: the directory for doxygen, paths from doxyfile are relative from here
      :return: False, if there is a deviation to the defined mandatory or optional settings.



.. py:function:: read_js_data_file(js_data_file: pathlib.Path) -> Any

   Read a doxygen javascript data file (e.g. menudata.js) and returns the data as json structure.

   :param js_data_file: The doxygen js data file to use.
   :return: a json like dict of the data.


.. py:class:: DoxygenOutputPathValidator

   Validates doxygen html output paths.


   .. py:attribute:: validation_msg
      :type:  str
      :value: ''



   .. py:method:: validate(doxygen_html_output: pathlib.Path) -> bool

      Validate a doxygen html output path.

      This is just meant to catch typos in paths etc. It will just check if a "doxygen.css" file is existing
      In the html output path.

      :param doxygen_html_output: The path where doxygen generates its html file to.
      :return: True if the path is valid else false.



