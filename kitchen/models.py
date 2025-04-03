from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )
    groups = models.ManyToManyField(Group, related_name="cook_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="cook_set", blank=True)

    def __str__(self) -> str:
        return self.username


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    dish_type = models.ForeignKey(
        DishType,
        related_name="dishes",
        on_delete=models.CASCADE
    )
    cooks = models.ManyToManyField(Cook, related_name="dishes")

    def __str__(self) -> str:
        return self.name
