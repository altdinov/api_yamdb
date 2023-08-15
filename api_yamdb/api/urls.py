from django.urls import include, path

from rest_framework import routers

from users.views import UserCreateViewSet, UserReceiveTokenViewSet, UserViewSet

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet
)

app_name = 'api'

router = routers.DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register("users", UserViewSet, basename="users")
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")
router.register("titles", TitleViewSet, basename="titles")

auth_urls = [
    path(
        "signup/", UserCreateViewSet.as_view({"post": "create"}), name="signup"
    ),
    path(
        "token/", UserReceiveTokenViewSet.as_view({"post": "create"}),
        name="token"
    ),
]

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include(auth_urls)),
]
