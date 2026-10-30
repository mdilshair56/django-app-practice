"""Reusable success-response helpers for API endpoints."""

from rest_framework import status
from rest_framework.response import Response


def success_response(
    *,
    data=None,
    message="Request successful.",
    status_code=status.HTTP_200_OK,
):
    """Return a consistent success response for non-paginated endpoints."""
    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


def paginated_success_response(
    *,
    data,
    count,
    next_page,
    previous_page,
    page,
    page_size,
    total_pages,
    message="Request successful.",
):
    """Return a consistent success response with pagination metadata."""
    return Response(
        {
            "success": True,
            "message": message,
            "data": data,
            "pagination": {
                "count": count,
                "next": next_page,
                "previous": previous_page,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
            },
        },
        status=status.HTTP_200_OK,
    )
