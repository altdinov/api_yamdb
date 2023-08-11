from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_year


class ModelForCategoryGenre(models.Model):

    name = models.CharField(max_length=256, verbose_name='Имя')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(ModelForCategoryGenre):

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(ModelForCategoryGenre):

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Имя')
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name='Год'
    )
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(
                limit_value=10, message='Рейтинг не может быть больше 10 баллов'
            ),
            MinValueValidator(
                limit_value=1, message='Рейтинг не может быть меньше 1го балла'
            )
        ],
        null=True,
        blank=True,
        verbose_name='Рейтинг'
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'
