"""
Пользователь
"""

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
import uuid

from django.db import models
from apps.common.abstract.abstract_base_save import AbstractBaseSave
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, AbstractBaseSave):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.CharField("Аккаунт", max_length=50, unique=True)
    email = models.EmailField("E-mail", unique=True)
    # Пароль был сгенерирован сервером или создан пользователем
    password_is_generate = models.BooleanField(default=True)
    remember_me = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # True - имеет доступ в админку

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"
        ordering = ("created_at",)
