from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.models import create_auth_token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        """Create user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """"Update user with using encrypted technology for password"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)

        user.save()
        return user


class UserListSerializer(UserSerializer):
    auth_token = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "last_name",
            "first_name",
            "is_staff",
            "auth_token",
        )
