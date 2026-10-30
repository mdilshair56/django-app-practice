"""Pagination configuration for Poll list responses."""

from rest_framework.pagination import PageNumberPagination

from common.api.responses import paginated_success_response


class PollPagination(PageNumberPagination):
    # Return ten polls by default and allow a bounded client override.
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        # Use the common response wrapper so list responses match other APIs.
        return paginated_success_response(
            data=data,
            count=self.page.paginator.count,
            next_page=self.get_next_link(),
            previous_page=self.get_previous_link(),
            page=self.page.number,
            page_size=self.get_page_size(self.request),
            total_pages=self.page.paginator.num_pages,
            message="Polls retrieved successfully.",
        )
