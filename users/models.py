from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from common.model_mixins import TimestampedModelMixin
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimestampedModelMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
