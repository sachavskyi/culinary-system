from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Dish

INDEX_URL = reverse("kitchen:index")


class PublicIndexViewTest(TestCase):
    def test_cook_login_required(self):
        res = self.client.get(INDEX_URL)
        self.assertNotEqual(res, 200)


class PrivateIndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test123",
        )
        self.client.force_login(self.user)

    def test_index_view_url_exists_at_desired_location(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)

    def test_index_view_url_accessible_by_name(self):
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.status_code, 200)

    def test_index_uses_correct_template_name(self):
        res = self.client.get(INDEX_URL)
        self.assertTemplateUsed(res, "kitchen/index.html")

    def test_index_has_correct_count_dish_types(self):
        numbers_of_dish_types = 7
        for dish_type_id in range(numbers_of_dish_types):
            DishType.objects.create(
                name=f"Test{dish_type_id}",
            )
        res = self.client.get(INDEX_URL)
        self.assertEqual(
            res.context["num_dish_types"],
            numbers_of_dish_types
        )

    def test_index_has_correct_count_dishes(self):
        dish_type = DishType.objects.create(
            name="pizza",
        )
        numbers_of_dishes = 8
        for dish_id in range(numbers_of_dishes):
            Dish.objects.create(
                name=f"Test{dish_id}",
                price=13,
                dish_type=dish_type,
            )
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.context["num_dishes"], numbers_of_dishes)

    def test_index_has_correct_count_cooks(self):
        numbers_of_cooks = 9
        for cook_id in range(numbers_of_cooks):
            get_user_model().objects.create_user(
                username=f"User{cook_id}",
                password="qwe",
                years_of_experience=cook_id,
            )
        res = self.client.get(INDEX_URL)
        self.assertEqual(res.context["num_cooks"], numbers_of_cooks + 1)

    def test_index_has_latest_dishes(self):
        dish_type = DishType.objects.create(
            name="pizza",
        )
        for dish_id in range(10):
            Dish.objects.create(
                name=f"Test{dish_id}",
                price=13,
                dish_type=dish_type,
            )
        res = self.client.get(INDEX_URL)
        self.assertContains(res, "Test9")
        self.assertContains(res, "Test8")
        self.assertContains(res, "Test5")
        self.assertNotContains(res, "Test4")
        self.assertNotContains(res, "Test1")
