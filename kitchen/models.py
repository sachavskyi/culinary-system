from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100)]
    )

    def __str__(self) -> str:
        return self.username
