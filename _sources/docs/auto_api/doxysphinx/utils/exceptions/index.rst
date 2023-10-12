:py:mod:`doxysphinx.utils.exceptions`
=====================================

.. py:module:: doxysphinx.utils.exceptions

.. autoapi-nested-parse::

   The exception module contains several standard exceptions.



Module Contents
---------------

.. py:exception:: ApplicationError(message)


   Bases: :py:obj:`Exception`

   .. autoapi-inheritance-diagram:: doxysphinx.utils.exceptions.ApplicationError
      :parts: 1

   A generic application error.


.. py:exception:: ValidationError(message)


   Bases: :py:obj:`Exception`

   .. autoapi-inheritance-diagram:: doxysphinx.utils.exceptions.ValidationError
      :parts: 1

   A generic error to indicate some validation failed.


.. py:exception:: PrerequisiteNotMetError(message)


   Bases: :py:obj:`Exception`

   .. autoapi-inheritance-diagram:: doxysphinx.utils.exceptions.PrerequisiteNotMetError
      :parts: 1

   An application error that indicates that some prerequisite is not met.


