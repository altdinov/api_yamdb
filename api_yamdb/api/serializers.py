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
        read_only_fields = ('title',)
        validators = (validators.UniqueTogetherValidator(
            queryset=Review.objects.all(),
            fields=('title', 'author'),
            message='Вы уже оценили данное произведение',
        ),)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('edited_date', 'review')


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
    rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title


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
