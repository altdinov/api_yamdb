from django.urls import include, path
from rest_framework import routers

from users.views import (
    UserCreateViewSet,
    UserReceiveTokenViewSet, UserViewSet
)

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

auth_urls = [
    path(
        'signup/',
        UserCreateViewSet.as_view({'post': 'create'}),
        name='signup'
    ),
    path(
        'token/',
        UserReceiveTokenViewSet.as_view({'post': 'create'}),
        name='token'
    )
]


urlpatterns = [
    path('auth/', include(auth_urls)),
    path('', include(router.urls))
]