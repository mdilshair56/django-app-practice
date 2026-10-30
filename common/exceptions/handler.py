"""Global exception handler for Django REST Framework APIs."""

import logging

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)


def _django_validation_detail(exc):
    """Convert Django ValidationError details into DRF-compatible details."""
    if hasattr(exc, "message_dict"):
        return exc.message_dict

    return {"non_field_errors": exc.messages}


def _get_error_message(exc, response_data):
    """Return a short, safe summary while preserving full details in errors."""
    if isinstance(exc, DRFValidationError):
        return "Validation failed."

    if isinstance(response_data, dict) and "detail" in response_data:
        return str(response_data["detail"])

    return "The request could not be completed."


def custom_exception_handler(exc, context):
    """
    Normalize API exceptions into one response shape.

    Expected response:
    {
        "success": false,
        "message": "...",
        "errors": {...},
        "status_code": 400
    }
    """
    if isinstance(exc, DjangoValidationError):
        exc = DRFValidationError(_django_validation_detail(exc))

    response = drf_exception_handler(exc, context)

    if response is None:
        request = context.get("request")
        view = context.get("view")

        logger.error(
            "Unhandled API exception in %s for %s",
            view.__class__.__name__ if view else "unknown view",
            getattr(request, "path", "unknown path"),
            exc_info=(type(exc), exc, exc.__traceback__),
        )

        return Response(
            {
                "success": False,
                "message": "An unexpected server error occurred.",
                "errors": None,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    response.data = {
        "success": False,
        "message": _get_error_message(exc, response.data),
        "errors": response.data,
        "status_code": response.status_code,
    }

    return response
