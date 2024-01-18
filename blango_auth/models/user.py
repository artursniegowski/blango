from django.contrib.auth.models import AbstractUser
from blango_auth.managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(
        _("email address"),
        unique=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
