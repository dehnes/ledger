from django.db import models
from django.conf import settings


class Person(models.Model):
    """A real-world entity (Human or Legal) that can own accounts."""

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # Link to the user who can log in as this person
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="person_profile",
    )

    class Meta:
        verbose_name_plural = "People"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
