from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType

DISH_TYPE_URL = reverse("kitchen:dish-type-list")


class PublicDishTypeTest(TestCase):
    def test_dish_type_login_required(self):
        res = self.client.get(DISH_TYPE_URL)
        self.assertNotEqual(res, 200)


class DishTypeListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        numbers_of_dish_types = 6
        for dish_type_id in range(numbers_of_dish_types):
            DishType.objects.create(
                name=f"test{dish_type_id}",
            )

    def test_dish_type_view_url_exists_at_desired_location(self):
        response = self.client.get("/dish_types/")
        self.assertEqual(response.status_code, 200)

    def test_dish_type_view_url_accessible_by_name(self):
        response = self.client.get(DISH_TYPE_URL)
        self.assertEqual(response.status_code, 200)

    def test_dish_type_uses_correct_template_name(self):
        res = self.client.get(DISH_TYPE_URL)
        self.assertTemplateUsed(res, "kitchen/dish_type_list.html")

    def test_dish_type_pagination_is_five(self):
        res = self.client.get(DISH_TYPE_URL)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["dish_type_list"]), 5)
        self.assertEqual(
            list(res.context["dish_type_list"]),
            list(DishType.objects.filter(pk__lte=5))
        )

    def test_lists_all_dish_types(self):
        res = self.client.get(DISH_TYPE_URL + "?page=2")
        self.assertEqual(res.status_code, 200)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["dish_type_list"]), 1)


class DishTypeCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.dish_type_create_url = reverse("kitchen:dish-type-create")

    def test_dish_type_create_view_url_exists_at_desired_location(self):
        res = self.client.get("/dish_types/create/")
        self.assertEqual(res.status_code, 200)

    def test_dish_type_create_view_url_accessible_by_name(self):
        res = self.client.get(self.dish_type_create_url)
        self.assertEqual(res.status_code, 200)

    def test_dish_type_create_uses_correct_template_name(self):
        res = self.client.get(self.dish_type_create_url)
        self.assertTemplateUsed(res, "kitchen/dish_type_form.html")

    def test_dish_type_create(self):
        res = self.client.post(
            self.dish_type_create_url,
            {"name": "pizza"}
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/dish_types/")
        self.assertEqual(DishType.objects.get(pk=1).name, "pizza")


class DishTypeUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(
            name="pizza",
        )
        self.dish_type_update_url = reverse(
            "kitchen:dish-type-update",
            args=[self.dish_type.id]
        )

    def test_dish_type_update_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/dish_types/{self.dish_type.id}/update/")
        self.assertEqual(res.status_code, 200)

    def test_dish_type_update_view_url_accessible_by_name(self):
        res = self.client.get(self.dish_type_update_url)
        self.assertEqual(res.status_code, 200)

    def test_dish_type_update_uses_correct_template_name(self):
        res = self.client.get(self.dish_type_update_url)
        self.assertTemplateUsed(res, "kitchen/dish_type_form.html")

    def test_dish_type_update(self):
        res = self.client.post(
            self.dish_type_update_url,
            {"name": "tea"}
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/dish_types/")
        self.assertEqual(self.dish_type.name, "pizza")
        self.dish_type.refresh_from_db()
        self.assertEqual(self.dish_type.name, "tea")


class DishTypeDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(
            name="pizza",
        )
        self.dish_type_delete_url = reverse(
            "kitchen:dish-type-delete",
            args=[self.dish_type.id]
        )

    def test_dish_type_delete_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/dish_types/{self.dish_type.id}/delete/")
        self.assertEqual(res.status_code, 200)

    def test_dish_type_delete_view_url_accessible_by_name(self):
        res = self.client.get(self.dish_type_delete_url)
        self.assertEqual(res.status_code, 200)

    def test_dish_type_delete_uses_correct_template_name(self):
        res = self.client.get(self.dish_type_delete_url)
        self.assertTemplateUsed(res, "kitchen/dish_type_delete_confirm.html")

    def test_dish_type_delete(self):
        res = self.client.post(self.dish_type_delete_url)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/dish_types/")
        self.assertFalse(DishType.objects.filter(id=self.dish_type.id))
