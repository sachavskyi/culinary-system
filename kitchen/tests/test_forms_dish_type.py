from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType


DISH_TYPE_URL = reverse("kitchen:dish-type-list")


class DishTypeSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        DishType.objects.create(name="pizza")
        DishType.objects.create(name="tea")

    def test_dish_type_search_without_query(self):
        res = self.client.get(DISH_TYPE_URL)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "pizza")
        self.assertContains(res, "tea")

    def test_dish_type_search_with_correct_query(self):
        res = self.client.get(DISH_TYPE_URL, {"search": "zza"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "pizza")
        self.assertNotContains(res, "tea")

    def test_dish_type_search_with_wrong_query(self):
        res = self.client.get(DISH_TYPE_URL, {"search": "YYY"})
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "pizza")
        self.assertNotContains(res, "tea")
