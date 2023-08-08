from django.contrib.auth import get_user_model
from django.db import models

from reviews.models import Review


User = get_user_model()


class Comment(models.Model):
    """Модель комментариев"""
    title = models.PositiveIntegerField(verbose_name='Произведение')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    review = models.ForeignKey(
        to=Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
        related_name='comments'
    )
    text = models.TextField(verbose_name='Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Опубликовано', auto_now_add=True
    )
    edited_date = models.DateTimeField(verbose_name='Изменено', auto_now=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
