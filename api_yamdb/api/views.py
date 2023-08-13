from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.serializers import ReviewSerializer, CommentSerializer
from reviews.models import Review, Category, Genre, Title
from .serializers import (
    CategorySerializer,
    GenreSerializer,
)
from .permissions import IsAdminOrModeratorOrOwnerOrReadOnly


class GetTitleMixin():
    def get_title(self):
        """Получение произведения по ID"""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title


class ReviewViewSet(ModelViewSet, GetTitleMixin):
    """Эндпоинт ревью"""
    serializer_class = ReviewSerializer
    # TODO: Заглушка до добавления пермишенов
    permission_classes = (
        IsAdminOrModeratorOrOwnerOrReadOnly,
    )

    def get_queryset(self):
        """Кверисет по id произведения"""
        title = self.get_title()
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        """Создание комментария"""
        title=self.get_title()
        serializer.save(
            author=self.request.user, title=title
        )
        self.get_serializer_context()

class CommentViewSet(ModelViewSet, GetTitleMixin):
    """Эндпоинт комментариев"""
    # TODO: Заглушка пока нужных пермишенов нет
    permission_classes = (
        IsAdminOrModeratorOrOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly
    )
    serializer_class = CommentSerializer

    def get_review(self, title):
        """Получение ревью по ID"""
        # TODO: Попробовать скормить кверисет от рилейтед тайтла
        return get_object_or_404(title.reviews, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        """Получаем комментарии по id произведения и id ревью"""
        title = self.get_title()
        review = self.get_review(title)
        return review.comments.all()

    def perform_create(self, serializer):
        """Создание ревью"""
        title = self.get_title()
        review = self.get_review(title)
        serializer.save(
            author=self.request.user,
            title=title,
            review=review,
        )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    #permission_classes = (OwnerOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    #permission_classes = (OwnerOrReadOnly,)
