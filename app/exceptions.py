"""
Custom exception used across the application.
"""


class NotFoundError(Exception):
    """A requested resource could not be found."""

    pass


class ValidationError(Exception):
    """Input data failed business-rule validation."""

    pass
