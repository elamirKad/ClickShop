from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy


class CustomAccountManager(BaseUserManager):
    """
    Custom user model manager
    """

    def create_user(
        self, email, user_name, first_name, second_name, password, **other_fields
    ):
        """
        Create and save a user with the given email and password
        """
        # Normalize the email address
        if not email:
            raise ValueError(gettext_lazy("invalid_email"))
        email = self.normalize_email(email)

        # Create the user
        user = self.model(
            email=email,
            user_name=user_name,
            first_name=first_name,
            second_name=second_name,
            **other_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self, email, user_name, first_name, second_name, password, **other_fields
    ):
        """
        Create and save a superuser with the given email and password
        """
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True")

        return self.create_user(
            email, user_name, first_name, second_name, password, **other_fields
        )


class NewUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    """

    email = models.EmailField(gettext_lazy("email address"), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    second_name = models.CharField(max_length=150)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(gettext_lazy("about"), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name", "first_name", "second_name"]

    def __str__(self):
        return self.user_name
