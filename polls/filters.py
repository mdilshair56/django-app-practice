"""Query-parameter filters for the Poll list endpoint."""

from django_filters import rest_framework as filters

from polls.models import Poll


class PollFilter(filters.FilterSet):
    # Filter polls using the choices already defined by the Poll model.
    status = filters.ChoiceFilter(choices=Poll.Status.choices)
    result_visibility = filters.ChoiceFilter(
        choices=Poll.ResultVisibility.choices
    )

    # Date/time filters use ISO 8601 query-parameter values.
    created_after = filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )
    created_before = filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )
    starts_after = filters.IsoDateTimeFilter(
        field_name="starts_at",
        lookup_expr="gte",
    )
    starts_before = filters.IsoDateTimeFilter(
        field_name="starts_at",
        lookup_expr="lte",
    )
    ends_after = filters.IsoDateTimeFilter(
        field_name="ends_at",
        lookup_expr="gte",
    )
    ends_before = filters.IsoDateTimeFilter(
        field_name="ends_at",
        lookup_expr="lte",
    )

    class Meta:
        model = Poll
        fields = [
            "status",
            "result_visibility",
        ]
