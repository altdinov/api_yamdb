from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from reviews.models import Category, Genre, Review, Title

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

    def get_queryset(self):
        """Кверисет по id произведения"""
        title = self._get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        """Создание ревью"""
        title = self._get_title()
        serializer.save(
            author=self.request.user, title=title
        )


class CommentViewSet(ModelViewSet, GetTitleMixin):
    """Эндпоинт комментариев"""
    permission_classes = (
        IsAdminOrModeratorOrOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly
    )
    serializer_class = CommentSerializer

    def _get_review(self):
        """Получение ревью по ID"""
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        """Получаем комментарии по id произведения и id ревью"""
        review = self._get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        """Создание комментария"""
        review = self._get_review()
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
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    permission_classes = (AdminOrReadOnly,)
    ordering = ('id',)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializerForWrite
        return TitleSerializer

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__score'))
