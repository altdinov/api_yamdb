from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            'год выпуска не может быть больше текущего'
        )
    if value < 0:
        raise ValidationError(
            'год выпуска не может быть отрицательным'
        )


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
