doxysphinx.utils.contexts
=========================

.. py:module:: doxysphinx.utils.contexts

.. autoapi-nested-parse::

   The contexts module contains several python context manager related functions.



Classes
-------

.. autoapisummary::

   doxysphinx.utils.contexts.TimedContext


Module Contents
---------------

.. py:class:: TimedContext

   Bases: :py:obj:`object`


   A context manager to measure elapsed time.

   Use it to measure the time taken to process the inner code.

   Usage:

   .. code-block: python

      with TimedContext() as tc:
          # do your thing here
          _logger.info(f"elapsed: {tc.elapsed_humanized()}.")


   .. py:method:: elapsed() -> datetime.timedelta

      Get the elapsed time.

      :return: The duration.



   .. py:method:: elapsed_humanized() -> str

      Get the elapsed time as a "humanized" format.

      :return: A humanized string of the elapsed time - Something like "3 days 5 hours 17 minutes".



