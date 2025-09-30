from django.contrib.auth import get_user_model
from django.test import TestCase

from kitchen.models import DishType, Dish


class DishTypeModelsTest(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(name="pizza")
        self.assertEqual(str(dish_type), dish_type.name)


class DishModelsTest(TestCase):
    def test_dish_str(self):
        dish_type = DishType.objects.create(name="pizza")
        dish = Dish.objects.create(
            name="pepperoni",
            price=10,
            dish_type=dish_type,
        )
        self.assertEqual(str(dish), dish.name)


class CookModelsTest(TestCase):
    def setUp(self):
        self.years_of_experience = 5
        self.user = get_user_model().objects.create_user(
            username="user",
            password='qwerty123',
            years_of_experience=self.years_of_experience,
        )

    def test_cook_str(self):
        self.assertEqual(str(self.user), self.user.username)

    def test_cook_has_years_of_experience(self):
        self.assertEqual(
            self.user.years_of_experience,
            self.years_of_experience
        )
