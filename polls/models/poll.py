from django.conf import settings
from django.db import models
from common.models import TimeFramedModel


class Poll(TimeFramedModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    class ResultVisibility(models.TextChoices):
        LIVE = 'live', 'Live'
        AFTER_SUBMISSION = 'after_submission', 'After Submission'
        POLLS_END = 'polls_end', 'Polls End'
        RESTRICTED = 'restricted', 'Restricted'

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_polls",
        # null=True,
        # blank=True,
    )
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    result_visibility = models.CharField(
        max_length=30,
        choices=ResultVisibility.choices,
        default=ResultVisibility.AFTER_SUBMISSION,
    )

    class Meta:
        verbose_name = "Poll"
        verbose_name_plural = "Polls"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name