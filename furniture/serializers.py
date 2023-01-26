from rest_framework import serializers

from furniture.models import (
    Furniture,
    Type,
    Commentary,
    Order,
    OrderItem,
)


class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = (
            "id",
            "model",
            "type",
            "price",
        )
        read_only_fields = ("id",)


class FurnitureCreateSerializer(FurnitureSerializer):
    class Meta:
        model = Furniture
        fields = (
            "id",
            "model",
            "type",
            "description",
            "price",
        )
        read_only_fields = ("id",)


class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = (
            "owner",
            "furniture",
            "created_time",
            "content",
        )


class FurnitureDetailSerializer(FurnitureSerializer):
    commentaries = CommentarySerializer(many=True, read_only=True)

    class Meta:
        model = Furniture
        fields = (
            "id",
            "model",
            "type",
            "description",
            "price",
            "length",
            "width",
            "height",
            "commentaries",
        )


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = (
            "id",
            "name",
        )


class CommentaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = (
            "content",
        )


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for nesting in OrderSerializer
    """
    class Meta:
        model = OrderItem
        fields = ("furniture", "amount")


class FurnitureOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = (
            "id",
            "model",
            "price",
        )


class OrderSerializer(serializers.ModelSerializer):
    furniture = FurnitureOrderSerializer(many=True)
    amount = OrderItemSerializer(source="orders", many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "furniture",
            "amount",
            "created_time",
        )
