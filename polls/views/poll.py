from rest_framework import filters as drf_filters
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from common.api.responses import success_response
from polls.filters import PollFilter
from polls.models import Poll
from polls.pagination import PollPagination
from polls.serializers.poll_serializer import PollDetailSerializer
from polls.services.poll import PollServices


class PollViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = PollDetailSerializer

    # Apply structured filters, text search, and client-selected ordering.
    filter_backends = [
        DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
    filterset_class = PollFilter
    search_fields = ["name", "description"]
    ordering_fields = [
        "name",
        "created_at",
        "starts_at",
        "ends_at",
    ]
    ordering = ["-created_at"]

    # Paginate only the Poll list endpoint.
    pagination_class = PollPagination

    def get_queryset(self):
        # Load related creator, questions, and options efficiently.
        return (
            Poll.objects
            .select_related("created_by")
            .prefetch_related(
                "poll_questions__question__answer_options"
            )
        )

    def create(self, request):
        created_poll = PollServices.mega_poll(
            poll_data=request.data,
            user=request.user,
        )

        poll_data = {
            "id": created_poll.pk,
            "name": created_poll.name,
            "description": created_poll.description,
            "status": created_poll.status,
            "result_visibility": created_poll.result_visibility,
            "questions": getattr(
                created_poll,
                "questions_data",
                [],
            ),
        }

        return success_response(
            data=poll_data,
            message="Poll created successfully.",
            status_code=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, *args, **kwargs):
        poll = self.get_object()
        serializer = self.get_serializer(poll)

        return success_response(
            data=serializer.data,
            message="Poll retrieved successfully.",
        )
