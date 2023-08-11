from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Кастомный класс User."""

    user = "user"
    moderator = "moderator"
    admin = "admin"
    ROLES = [(user, "user"), (admin, "admin"), (moderator, "moderator")]

    username = models.CharField(
        max_length=150,
        verbose_name="Имя пользователя",
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[\w.@+-]+$",
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
        max_length=20, verbose_name="Роль", choices=ROLES, default=user
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
        return self.role == self.admin or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.moderator

    @property
    def is_user(self):
        return self.role == self.user
