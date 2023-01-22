from rest_framework import viewsets

from furniture.models import (
    Furniture,
    Type,
    Order,
    Commentary,
)
from furniture.serializers import (
    FurnitureSerializer,
    TypeSerializer,
    OrderSerializer,
    CommentarySerializer,
)


class FurnitureViewSet(viewsets.ModelViewSet):
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class CommentaryViewSet(viewsets.ModelViewSet):
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
