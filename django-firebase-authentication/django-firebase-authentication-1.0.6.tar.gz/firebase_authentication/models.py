from django.db import models

from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _

__all__ = "User",


class User(AbstractUser):

    id = models.CharField(
        max_length=28,
        primary_key=True,
        db_index=True,
        unique=True
    )
    username = None
    email = models.EmailField(
        _('email address'),
        unique=True
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        name_str = f"{self.first_name} {self.last_name}".strip()
        return name_str or self.email
