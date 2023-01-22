from rest_framework import serializers

from furniture.models import Furniture, Type, Commentary, Order


class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = (
            "id",
            "model",
            "type",
            "description",
            "price",
            "comments"
        )
        read_only_fields = ("id",)


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = (
            "id",
            "name",
        )


class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = (
            "owner",
            "furniture",
            "content",
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            "furniture",
            "user",
            "created_at",
        )