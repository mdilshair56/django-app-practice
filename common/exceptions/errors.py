"""Application-wide API exception classes."""

from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError as DRFValidationError


class APIValidationError(DRFValidationError):
    """
    Validation error raised by application services.

    """


class ResourceNotFoundError(APIException):
    """Use when the requested resource does not exist."""

    status_code = 404
    default_detail = "The requested resource was not found."
    default_code = "not_found"


class ConflictError(APIException):
    """Use when a request conflicts with the current state of a resource."""

    status_code = 409
    default_detail = "The request conflicts with the current resource state."
    default_code = "conflict"
