from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=256,
    )
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=256,
    )
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=256,
    )
    year = serializers.IntegerField()
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title


class StringListField(serializers.ListField):
    child = serializers.CharField()


class TitleSerializerForWrite(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=256,
    )
    year = serializers.IntegerField()
    category = serializers.CharField()
    genre = StringListField(write_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title
