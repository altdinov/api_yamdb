from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404

from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsSuperUserOrIsAdmin
from .serializers import (
    UserCreateSerializer,
    UserRecieveTokenSerializer,
    UserSerializer
)
from .utils import send_confirmation_code


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if User.objects.filter(
            username=request.data.get("username"),
            email=request.data.get("email")
        ):
            user = User.objects.get(username=request.data.get("username"))
            serializer = UserCreateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            username = request.data.get("username")
            user = User.objects.get(username=username)
            confirmation_code = default_token_generator.make_token(user)
            send_confirmation_code(
                email=user.email, confirmation_code=confirmation_code
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserReceiveTokenViewSet(mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRecieveTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        confirmation_code = serializer.validated_data.get("confirmation_code")
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = {"confirmation_code": "Неверный код подтверждения"}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {"token": str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)


class UserViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUserOrIsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)

    @action(
        detail=False,
        methods=["get", "patch", "delete"],
        url_path=r"(?P<username>[\w.@+-]+)",
        url_name="get_user",
    )
    def get_user_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.method == "PATCH":
            serializer = self.serializer_class(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get", "patch"],
        url_path="me",
        url_name="me",
        permission_classes=(permissions.IsAuthenticated,),
    )
    def get_me_data(self, request):
        if request.method == "PATCH":
            serializer = self.serializer_class(
                request.user,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
