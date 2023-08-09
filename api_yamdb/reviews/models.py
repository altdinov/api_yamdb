from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


User = get_user_model()


class BasePost(models.Model):
    """Базовая абстрактная модель для наследования в ревью и комментариях"""
    title = models.PositiveIntegerField(
        verbose_name='Произведение',
    )
    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Опубликовано', auto_now_add=True
    )
    edited_date = models.DateTimeField(verbose_name='Изменено', auto_now=True)

    class Meta:
        abstract = True

class Review(BasePost):
    """Модель Ревью"""
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


    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['title', 'author'],
            name='Only_one_review_from_author_for_title'
        )]
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'


class Comment(BasePost):
    """Модель комментариев"""

    review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
