from django.contrib.auth.models import AbstractUser
from django.db import models

from furniture_service import settings


class Furniture(models.Model):
    model = models.CharField(max_length=64)
    type = models.ForeignKey(
        "Type",
        on_delete=models.DO_NOTHING,
        related_name="furnitures",
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=3)
    comments = models.ForeignKey(
        "Commentary",
        on_delete=models.CASCADE,
        related_name="furnitures",
    )


class Type(models.Model):
    name = models.CharField(max_length=255)


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
    content = models.TextField()


class Order(models.Model):
    furniture = models.ManyToManyField(Furniture)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now=True)
