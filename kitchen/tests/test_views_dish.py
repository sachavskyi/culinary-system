from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from kitchen.models import DishType, Dish

DISH_URL = reverse("kitchen:dish-list")


class PublicDishTest(TestCase):
    def test_dish_login_required(self):
        res = self.client.get(DISH_URL)
        self.assertNotEqual(res, 200)


class DishListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        dish_type = DishType.objects.create(name="pizza")
        numbers_of_dishes = 6
        for dish_id in range(numbers_of_dishes):
            Dish.objects.create(
                name=f"test{dish_id}",
                price=10,
                dish_type=dish_type,
            )

    def test_dish_view_url_exists_at_desired_location(self):
        response = self.client.get("/dishes/")
        self.assertEqual(response.status_code, 200)

    def test_dish_view_url_accessible_by_name(self):
        response = self.client.get(DISH_URL)
        self.assertEqual(response.status_code, 200)

    def test_dish_uses_correct_template_name(self):
        res = self.client.get(DISH_URL)
        self.assertTemplateUsed(res, "kitchen/dish_list.html")

    def test_dish_pagination_is_five(self):
        res = self.client.get(DISH_URL)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["dish_list"]), 5)
        self.assertEqual(
            list(res.context["dish_list"]),
            list(Dish.objects.order_by("-pk")[:5])
        )

    def test_lists_all_dishes(self):
        res = self.client.get(DISH_URL + "?page=2")
        self.assertEqual(res.status_code, 200)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["dish_list"]), 1)


class DishCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.dish_create_url = reverse("kitchen:dish-create")

    def test_dish_create_view_url_exists_at_desired_location(self):
        res = self.client.get("/dishes/create/")
        self.assertEqual(res.status_code, 200)

    def test_dish_create_view_url_accessible_by_name(self):
        res = self.client.get(self.dish_create_url)
        self.assertEqual(res.status_code, 200)

    def test_dish_create_uses_correct_template_name(self):
        res = self.client.get(self.dish_create_url)
        self.assertTemplateUsed(res, "kitchen/dish_form.html")

    def test_dish_create(self):
        dish_type = DishType.objects.create(name="pizza")
        res = self.client.post(
            self.dish_create_url,
            {
                "name": "pepperoni",
                "price": 10,
                "dish_type": dish_type.id,
            }
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/dishes/")
        self.assertEqual(Dish.objects.get(pk=1).name, "pepperoni")


class DishUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(name="pizza")
        self.dish = Dish.objects.create(
            name="pepperoni",
            price=10,
            dish_type=self.dish_type,
        )
        self.dish_update_url = reverse(
            "kitchen:dish-update",
            args=[self.dish.id]
        )

    def test_dish_update_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/dishes/{self.dish.id}/update/")
        self.assertEqual(res.status_code, 200)

    def test_dish_update_view_url_accessible_by_name(self):
        res = self.client.get(self.dish_update_url)
        self.assertEqual(res.status_code, 200)

    def test_dish_update_uses_correct_template_name(self):
        res = self.client.get(self.dish_update_url)
        self.assertTemplateUsed(res, "kitchen/dish_form.html")

    def test_dish_update(self):
        res = self.client.post(
            self.dish_update_url,
            {
                "name": "margarita",
                "price": 10,
                "dish_type": self.dish.dish_type.id,
            }
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/dishes/")
        self.assertEqual(self.dish.name, "pepperoni")
        self.dish.refresh_from_db()
        self.assertEqual(self.dish.name, "margarita")


class DishDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        dish_type = DishType.objects.create(name="pizza")
        self.dish = Dish.objects.create(
            name="pepperoni",
            price=10,
            dish_type=dish_type,
        )
        self.dish_delete_url = reverse(
            "kitchen:dish-delete",
            args=[self.dish.id]
        )

    def test_dish_delete_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/dishes/{self.dish.id}/delete/")
        self.assertEqual(res.status_code, 200)

    def test_dish_delete_view_url_accessible_by_name(self):
        res = self.client.get(self.dish_delete_url)
        self.assertEqual(res.status_code, 200)

    def test_dish_delete_uses_correct_template_name(self):
        res = self.client.get(self.dish_delete_url)
        self.assertTemplateUsed(res, "kitchen/dish_delete_confirm.html")

    def test_dish_delete(self):
        res = self.client.post(self.dish_delete_url)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/dishes/")
        self.assertFalse(Dish.objects.filter(id=self.dish.id))
