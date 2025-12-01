"""Custom exceptions for multibase encoding/decoding errors."""


class MultibaseError(ValueError):
    """Base exception for all multibase errors."""

    pass


class UnsupportedEncodingError(MultibaseError):
    """Raised when an encoding is not supported."""

    pass


class InvalidMultibaseStringError(MultibaseError):
    """Raised when a multibase string is invalid or cannot be decoded."""

    pass


class DecodingError(MultibaseError):
    """Raised when decoding fails."""

    pass
