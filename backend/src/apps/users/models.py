from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not False:
            if extra_fields.get("is_superuser") is not False:
                return self._create_user(email, password, **extra_fields)

        raise ValueError("Superuser must have is_staff=True and is_superuser=True.")


class User(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField("email address", unique=True)

    USERNAME_FIELD = "email"  # Use email to log in
    REQUIRED_FIELDS = []  # Removes email from required fields for createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email
