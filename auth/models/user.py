from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        CLIENT = "client", "Client"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENT,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    # REQUIRED_FIELDS = [
    #     "email",
    #     "first_name",
    #     "last_name",
    #     "phone_number",
    # ]

    def __str__(self):
        return self.username