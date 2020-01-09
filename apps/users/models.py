"""
Пользователь

MANAGER - доступ ко всей информации (только чтение).
OPERATOR - доступ ко всей информации (только чтение, редактирование).
CHIEF_OPERATOR(Главный оператор) - доступ ко всей информации без ограничений.
IT_DEVELOPER(IT разработчик/владелец) - доступ ко всей информации без ограничений.

После выполнения всех миграций и fixtures права добавляются автоматически
в файле admin_panel_init_data.py
"""

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
import uuid

from django.db import models
from apps.common.abstract.abstract_base_save import AbstractBaseSave
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, AbstractBaseSave):
    MANAGER, OPERATOR, CHIEF_OPERATOR, IT_DEVELOPER = 1, 2, 3, 4

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.CharField("Аккаунт", max_length=50, unique=True)
    email = models.EmailField("E-mail", unique=True)
    first_name = models.CharField("Имя", max_length=50, blank=True)
    last_name = models.CharField("Фамилия", max_length=50, blank=True)
    # Пароль был сгенерирован сервером или создан пользователем
    password_is_generate = models.BooleanField(default=True)
    remember_me = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "users"
        ordering = ("created_at",)
