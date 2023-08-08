from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from api.serializers import ReviewSerializer, CommentSerializer
from reviews.models import Review


class ReviewViewSet(ModelViewSet):
    """Эндпоинт ревью"""
    serializer_class = ReviewSerializer
    # TODO: Заглушка до добавления пермишенов
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_title(self):
        # TODO: добавить модель произведений
        # title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return self.kwargs.get('title_id')

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

class CommentViewSet(ModelViewSet):
    """Эндпоинт комментариев"""
    # TODO: Заглушка пока нужных пермишенов нет
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Получаем комментарии по id произведения и id ревью"""
        # TODO: добавить модель произведений
        # title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        # TODO: Попробовать скормить кверисет от рилейтед тайтла
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        """Создание ревью"""
        # TODO: добавить модель произведений
        # title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        # TODO: Попробовать скормить кверисет от рилейтед тайтла
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user,
            title=self.kwargs.get('title_id'),
            review=review,
        )
