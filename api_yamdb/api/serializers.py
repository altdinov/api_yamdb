from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title
from reviews.validators import validate_year


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

    def validate(self, attrs):
        validate_year(attrs['year'])
        return attrs

    def create(self, validated_data):
        print(validated_data)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title
        lookup_field = 'slug'
