doxysphinx.utils.iterators
==========================

.. py:module:: doxysphinx.utils.iterators

.. autoapi-nested-parse::

   The iterators module contains several iterator related helper functions.



Attributes
----------

.. autoapisummary::

   doxysphinx.utils.iterators.T
   doxysphinx.utils.iterators.Predicate
   doxysphinx.utils.iterators.Action


Functions
---------

.. autoapisummary::

   doxysphinx.utils.iterators.apply_if
   doxysphinx.utils.iterators.apply_if_first
   doxysphinx.utils.iterators.apply


Module Contents
---------------

.. py:data:: T

.. py:data:: Predicate

.. py:data:: Action

.. py:function:: apply_if(iterable: Iterable[T], check: Predicate[T], action: Action[T])

   Apply the action function to each element that matches the predicate.

   :param iterable: The input iterable (list etc...)
   :param check: The predicate to check
   :param action: The action to apply


.. py:function:: apply_if_first(iterable: Iterable[T], check: Predicate[T], action: Action[T])

   Apply the action function to the first element that matches the predicate.

   :param iterable: The input iterable (list etc...)
   :param check: The predicate to check
   :param action: The action to apply


.. py:function:: apply(iterable: Iterable[T], action: Action[T]) -> None

   Apply the action function to all elements.

   :param iterable: The input iterable (list etc...)
   :param action: The action to apply


