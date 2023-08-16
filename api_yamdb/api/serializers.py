from rest_framework import serializers
from rest_framework import validators

from reviews.models import Category, Comment, Genre, Review, Title

from .utils import CurrentDefaultTitle


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор ревью"""
    author = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=CurrentDefaultTitle())

    class Meta:
        model = Review
        exclude = ('edited_date',)
        read_only_fields = ('pub_date', 'title')
        validators = (validators.UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=('title', 'author'),
            message='Вы уже оценили данное произведение',
        ),)

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
        exclude = ('edited_date', 'review')
        read_only_fields = ('pub_date',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""
    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""
    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для операций чтения"""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField(
        method_name='rating_calculation'
    )

    class Meta:
        fields = '__all__'
        model = Title

    def rating_calculation(self, obj):
        return None


class TitleSerializerForWrite(serializers.ModelSerializer):
    """Сериализатор произведений для операций записи"""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title
