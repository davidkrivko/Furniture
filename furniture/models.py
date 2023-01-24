from django.contrib.auth.models import AbstractUser
from django.db import models

from furniture.media_path import image_file_path
from furniture_service import settings


class Furniture(models.Model):
    model = models.CharField(max_length=64)
    type = models.ForeignKey(
        "Type",
        on_delete=models.DO_NOTHING,
        related_name="furnitures",
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    photo = models.ImageField(null=True, upload_to=image_file_path)
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    length = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.model}, {self.price}"


class Type(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Commentary(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        related_name="commentaries",
    )
    furniture = models.ForeignKey(
        Furniture,
        on_delete=models.CASCADE,
        related_name="commentaries",
    )
    created_time = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta:
        ordering = ["-created_time"]


class Order(models.Model):
    furniture = models.ManyToManyField(Furniture, through="OrderItem")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    created_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_time"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orders")
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name="furnitures")
    amount = models.IntegerField(default=1)

    class Meta:
        verbose_name = "order_item"
        db_table = "furniture_order_item"
