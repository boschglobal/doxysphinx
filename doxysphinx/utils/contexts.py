# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""The contexts module contains several python context manager related functions."""

from datetime import timedelta
from timeit import default_timer as timer


class TimedContext(object):
    """
    A context manager to measure elapsed time.

    Use it to measure the time taken to process the inner code.

    Usage:

    .. code-block: python

       with TimedContext() as tc:
           # do your thing here
           _logger.info(f"elapsed: {tc.elapsed_humanized()}.")
    """

    def __init__(self):
        """Create an instance of the TimedContext."""
        self._start: float = 0
        self._elapsed = timedelta()

    def elapsed(self) -> timedelta:
        """
        Get the elapsed time.

        :return: The duration.
        """
        return self._elapsed

    def elapsed_humanized(self) -> str:
        """
        Get the elapsed time as a "humanized" format.

        :return: A humanized string of the elapsed time - Something like "3 days 5 hours 17 minutes".
        """
        data = {}
        data["days"], remaining = divmod(self._elapsed.total_seconds(), 86_400)
        data["hours"], remaining = divmod(remaining, 3_600)
        data["minutes"], data["seconds"] = divmod(remaining, 60)

        time_segments = ((name, round(value)) for name, value in data.items())
        time_parts = [f"{value} {name[:-1] if value == 1 else name}" for name, value in time_segments if value > 0]
        if time_parts:
            return " ".join(time_parts)
        else:
            return "below 1 second"

    def __enter__(self):
        """Context manager enter method."""
        self._start = timer()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit method."""
        self._elapsed = timedelta(seconds=timer() - self._start)
        pass
