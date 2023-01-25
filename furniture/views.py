from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from furniture.models import (
    Furniture,
    Type,
    Order,
    Commentary, OrderItem,
)
from furniture.permissions import IsAdminOrReadOnlyAuthenticated
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
    permission_classes = (IsAdminOrReadOnlyAuthenticated, )

    @staticmethod
    def _params_to_ints(qs):
        """
            Split parameters from request
        """
        return [int(str_id) for str_id in qs.split(",")]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FurnitureDetailSerializer
        if self.action == "add_commentary":
            return CommentaryCreateSerializer
        return FurnitureSerializer

    def get_queryset(self):
        """
        Add filtering by types
        """
        queryset = self.queryset

        type_obj = self.request.query_params.get("type")

        if type_obj:
            type_ids = self._params_to_ints(type_obj)
            queryset = queryset.filter(type__id__in=type_ids)

        return queryset

    @action(detail=True, methods=["post"])
    def add_commentary(self, request, pk=None):
        """
        Extra action for add commentaries
        """
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
    permission_classes = (IsAdminOrReadOnlyAuthenticated,)


class CommentaryViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    queryset = Commentary.objects.all()
    serializer_class = CommentarySerializer

    def perform_create(self, serializer):
        """
        Using authenticated user
        """
        serializer.save(user=self.request.user.id)


class OrderPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Show just users orders
        """
        return self.queryset.filter(user=self.request.user.id).prefetch_related("furniture", "orders__furniture")

    def perform_create(self, serializer):
        """
        Using authenticated user
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Redefine create method for using
        already created furniture objects
        """
        data = request.data

        new_order = Order.objects.create(user=request.user)
        new_order.save()

        for i in range(len(data["furniture"])):
            furniture_obj = Furniture.objects.get(id=data["furniture"][i])
            item = OrderItem.objects.create(order=new_order, furniture=furniture_obj, amount=data["amount"][i])
            item.save()
        serializer = OrderSerializer(new_order)

        return Response(serializer.data)
