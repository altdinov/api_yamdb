from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from api_yamdb.settings import FORBIDDEN_CHAR


class User(AbstractUser):
    """Кастомный класс User."""

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    ROLES = [(USER, "user"), (ADMIN, "admin"), (MODERATOR, "moderator")]

    username = models.CharField(
        max_length=150,
        verbose_name="Имя пользователя",
        unique=True,
        validators=[
            RegexValidator(
                regex=FORBIDDEN_CHAR,
                message=("Имя пользователя содержит недопустимый символ"),
            )
        ],
    )
    email = models.EmailField(
        max_length=254, verbose_name="email", unique=True
    )
    first_name = models.CharField(
        max_length=150, verbose_name="Имя", blank=True
    )
    last_name = models.CharField(
        max_length=150, verbose_name="Фамилия", blank=True
    )
    bio = models.TextField(verbose_name="Биография", blank=True)
    role = models.CharField(
        max_length=20, verbose_name="Роль", choices=ROLES, default=USER
    )
    password = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
