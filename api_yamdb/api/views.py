from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, GenreTitle, Review, Title

from .filters import TitleFilter
from .permissions import AdminOrReadOnly, IsAdminOrModeratorOrOwnerOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleSerializerForWrite,
)


class GetTitleMixin():
    def _get_title(self):
        """Получение произведения по ID"""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title


class ReviewViewSet(ModelViewSet, GetTitleMixin):
    """Эндпоинт ревью"""
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAdminOrModeratorOrOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )

    def _update_rating(self, title):
        title.rating = round(
            title.reviews.aggregate(Avg('score'))['score__avg'], 0
        )
        title.save()

    def get_queryset(self):
        """Кверисет по id произведения"""
        title = self._get_title()
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        """Создание ревью"""
        title = self._get_title()
        serializer.save(
            author=self.request.user, title=title
        )
        self._update_rating(title)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        title = self._get_title()
        self._update_rating(title)


class CommentViewSet(ModelViewSet, GetTitleMixin):
    """Эндпоинт комментариев"""
    permission_classes = (
        IsAdminOrModeratorOrOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly
    )
    serializer_class = CommentSerializer

    def _get_review(self, title):
        """Получение ревью по ID"""
        return get_object_or_404(
            title.reviews, pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        """Получаем комментарии по id произведения и id ревью"""
        title = self._get_title()
        review = self._get_review(title)
        return review.comments.all()

    def perform_create(self, serializer):
        """Создание комментария"""
        title = self._get_title()
        review = self._get_review(title)
        serializer.save(
            author=self.request.user,
            review=review,
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
