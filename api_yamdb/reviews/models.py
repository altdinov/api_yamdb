from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


User = get_user_model()


class Review(models.Model):
    """Модель Ревью"""
    title = models.PositiveIntegerField(
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MaxValueValidator(
                limit_value=10, message='Оценка не может быть больше 10 баллов'
            ),
            MinValueValidator(
                limit_value=1, message='Оценка не может быть меньше 1го балла'
            )
        ]
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Опубликовано', auto_now_add=True
    )
    edited_date = models.DateTimeField(verbose_name='Изменено', auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'],
            name='Only_one_review_from_author_for_title'
        )]
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
