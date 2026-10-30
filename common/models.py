from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from datetime import timedelta

def get_default_ends_at():
    return timezone.now() + timedelta(days=1)

class TimeStampedModel(models.Model):
    """Base model for creation and update timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TimeFramedModel(TimeStampedModel):
    """Base model adding starts_at, ends_at, and date sequence validation."""
    # Add defaults here. DRF will automatically make them optional in your API.
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField(default=get_default_ends_at)

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
            raise ValidationError({'ends_at': 'End time must be after start time.'})