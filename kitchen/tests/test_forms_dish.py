from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Dish


DISH_URL = reverse("kitchen:dish-list")


class DishSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        dish_type = DishType.objects.create(name="pizza")
        Dish.objects.create(
            name="pepperoni",
            price=10,
            dish_type=dish_type,
        )
        Dish.objects.create(
            name="margarita",
            price=10,
            dish_type=dish_type,
        )

    def test_dish_search_without_query(self):
        res = self.client.get(DISH_URL)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "pepperoni")
        self.assertContains(res, "margarita")

    def test_dish_search_with_correct_query(self):
        res = self.client.get(DISH_URL, {"search": "marg"})
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "pepperoni")
        self.assertContains(res, "margarita")

    def test_dish_search_with_wrong_query(self):
        res = self.client.get(DISH_URL, {"search": "YYY"})
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "pepperoni")
        self.assertNotContains(res, "margarita")
