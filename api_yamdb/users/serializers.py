from rest_framework import serializers

from .models import User


class BaseUser(serializers.ModelSerializer):

    def validate_username(self, data):
        if self.initial_data.get('username') == 'me':
            raise serializers.ValidationError("Использовать имя me запрещено")
        return data


class UserCreateSerializer(BaseUser):
    class Meta:
        model = User
        fields = ("username", "email")


class UserRecieveTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )
    confirmation_code = serializers.CharField(max_length=150, required=True)


class UserSerializer(BaseUser):
    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "bio", "role"
        )
