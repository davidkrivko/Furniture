from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from furniture.models import (
    Furniture,
    Type,
    Order,
    Commentary, OrderItem,
)
from furniture.serializers import (
    FurnitureSerializer,
    TypeSerializer,
    OrderSerializer,
    CommentarySerializer,
    FurnitureDetailSerializer,
    CommentaryCreateSerializer,
)


class FurnitureViewSet(viewsets.ModelViewSet):
    queryset = Furniture.objects.all()
    serializer_class = FurnitureSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FurnitureDetailSerializer
        if self.action == "add_commentary":
            return CommentaryCreateSerializer
        return FurnitureSerializer

    @action(detail=True, methods=["post"])
    def add_commentary(self, request, pk=None):
        user = request.user
        furniture = self.get_object()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["owner"] = user
            serializer.validated_data["furniture"] = furniture
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST,
                        )


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class CommentaryViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.id)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data

        new_order = Order.objects.create(user=request.user)
        new_order.save()

        for i in range(len(data["furniture"])):
            furniture_obj = Furniture.objects.get(id=data["furniture"][i])
            item = OrderItem.objects.create(order=new_order, furniture=furniture_obj, amount=data["amount"][i])
            item.save()
        serializer = OrderSerializer(new_order)

        return Response(serializer.data)
