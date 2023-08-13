from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            'год выпуска не может быть больше текущего'
        )
    if value < 0:
        raise ValidationError(
            'год выпуска не может быть отрицательным'
        )
