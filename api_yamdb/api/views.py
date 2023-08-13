from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from reviews.models import Category, Genre, GenreTitle, Title

from .filters import TitleFilter
from .permissions import AdminOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleSerializerForWrite
)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)
    ordering = ('id',)


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    permission_classes = (AdminOrReadOnly,)
    ordering = ('id',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    permission_classes = (AdminOrReadOnly,)
    ordering = ('id',)

    def create(self, request, *args, **kwargs):
        self.serializer_class = TitleSerializerForWrite
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        genres_slug_list = serializer.validated_data.pop('genre')
        category = get_object_or_404(
            Category, slug=serializer.validated_data.pop('category')
        )
        serializer.save(category=category)

        title = get_object_or_404(Title, id=serializer.data['id'])
        for genre_slug in genres_slug_list:
            genre = get_object_or_404(Genre, slug=genre_slug)
            GenreTitle.objects.create(
                title=title, genre=genre
            )
        self.serializer_class = TitleSerializer
        serializer = self.serializer_class(title)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        self.serializer_class = TitleSerializerForWrite
        title = get_object_or_404(Title, id=pk)
        serializer = self.serializer_class(
            title, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        if 'category' in serializer.validated_data:
            category = get_object_or_404(
                Category, slug=serializer.validated_data.pop('category')
            )
            serializer.save(category=category)
        else:
            serializer.save()

        if 'genre' in serializer.validated_data:
            genres_slug_list = serializer.validated_data.pop('genre')
            GenreTitle.objects.filter(title_id=pk).delete()
            for genre_slug in genres_slug_list:
                genre = get_object_or_404(Genre, slug=genre_slug)
                GenreTitle.objects.create(
                    title=title, genre=genre
                )

        self.serializer_class = TitleSerializer
        serializer = self.serializer_class(title)
        return Response(serializer.data, status=status.HTTP_200_OK)
