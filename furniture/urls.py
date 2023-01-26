from django.urls import path, include
from rest_framework import routers

from furniture.views import (
    FurnitureViewSet,
    TypeViewSet,
    CommentaryViewSet,
    OrderViewSet,
)

router = routers.DefaultRouter()
router.register("furniture", FurnitureViewSet)
router.register("types", TypeViewSet)
router.register("commentaries", CommentaryViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls))
]

app_name = "furniture"
