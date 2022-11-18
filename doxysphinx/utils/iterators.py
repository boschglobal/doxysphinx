# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""The iterators module contains several iterator related helper functions."""

from typing import Callable, Iterable, TypeVar

T = TypeVar("T")

Predicate = Callable[[T], bool]
Action = Callable[[T], None]


def apply_if(iterable: Iterable[T], check: Predicate[T], action: Action[T]):
    """Apply the action function to each element that matches the predicate.

    :param iterable: The input iterable (list etc...)
    :param check: The predicate to check
    :param action: The action to apply
    """
    while found := next((p for p in iterable if check(p)), None) is not None:
        action(found)  # type: ignore [arg-type]


def apply_if_first(iterable: Iterable[T], check: Predicate[T], action: Action[T]):
    """Apply the action function to the first element that matches the predicate.

    :param iterable: The input iterable (list etc...)
    :param check: The predicate to check
    :param action: The action to apply
    """
    found = next((p for p in iterable if check(p)), None)
    if found is not None:
        action(found)


def apply(iterable: Iterable[T], action: Action[T]) -> None:
    """Apply the action function to all elements.

    :param iterable: The input iterable (list etc...)
    :param action: The action to apply
    """
    for item in iterable:
        action(item)
