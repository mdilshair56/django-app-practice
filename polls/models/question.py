from django.conf import settings
from django.db import models
from common.models import TimeStampedModel

class Question(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="questions",
    )

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["created_by", "name"],
                name="unique_question_per_user",
            )
        ]

    def __str__(self):
        return self.name