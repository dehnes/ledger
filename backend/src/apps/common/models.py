from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    iso_code = models.CharField(
        max_length=2, unique=True, help_text="ISO 3166-1 alpha-2 (e.g., DE)"
    )
    iso_code_3 = models.CharField(
        max_length=3, unique=True, help_text="ISO 3166-1 alpha-3 (e.g., DEU)"
    )
    is_eu_member = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.iso_code})"
