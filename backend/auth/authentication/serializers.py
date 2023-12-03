from rest_framework import serializers
from .models import CustomUserModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPair(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["is_superuser"] = user.is_superuser
        token["is_active"] = user.is_active
        token["is_staff"] = user.is_staff
        token["is_external"] = user.is_external

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data["username"] = user.username
        data["is_superuser"] = user.is_superuser
        data["is_active"] = user.is_active
        data["is_staff"] = user.is_staff
        data["is_external"] = user.is_external
        # ... add other user information as needed

        return data


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = "__all__"
