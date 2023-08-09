from rest_framework import serializers
from rest_framework import validators

from reviews.models import Review, Comment
from .utils import CurrentDefaultTitle


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор ревью"""
    author = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=CurrentDefaultTitle())


    class Meta:
        model = Review
        # fields ='__all__'
        exclude = ('edited_date',)
        read_only_fields = ('pub_date', 'title')
        validators = (validators.UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=('title', 'author'),
            message='Вы уже оценили данное произведение',
        ),)

    def validate(self, attrs):
        """validate_score почему-то не вызывается поэтому проводим валидацию
        в этом методе"""
        if not (1 <= attrs['score'] <= 10):
            raise serializers.ValidationError(
                detail={'score': 'Оценка должна быть от 1 до 10'}
            )
        return attrs

    def validate_score(self, value):
        """Проверяем чтобы оценка была в допустимом диапазоне"""
        if not (1 <= value <= 10):
            raise serializers.ValidationError(
                detail='Оценка должна быть от 1 до 10'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        exclude = ('edited_date', 'review', 'title')
        read_only_fields = ('pub_date',)
