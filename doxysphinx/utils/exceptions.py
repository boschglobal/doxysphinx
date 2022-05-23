# =====================================================================================
#  C O P Y R I G H T
# -------------------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  Author(s):
#  - Markus Braun, :em engineering methods AG (contracted by Robert Bosch GmbH)
# =====================================================================================
"""The exception module contains several standard exceptions."""

# just some exception classes


class ApplicationError(Exception):
    """A generic application error."""

    def __init__(self, message):
        """Exception constructor."""
        super().__init__(message)


class ValidationError(Exception):
    """A generic error to indicate some validation failed."""

    def __init__(self, message):
        """Exception constructor."""
        super().__init__(message)


class PrerequisiteNotMetError(Exception):
    """An application error that indicates that some prerequisite is not met."""

    def __init__(self, message):
        """Exception constructor."""
        super().__init__(message)
