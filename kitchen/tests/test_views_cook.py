from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

COOK_URL = reverse("kitchen:cook-list")


class PublicCookTest(TestCase):
    def test_cook_login_required(self):
        res = self.client.get(COOK_URL)
        self.assertNotEqual(res, 200)


class CookListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        numbers_of_cooks = 6
        for cook_id in range(numbers_of_cooks):
            get_user_model().objects.create_user(
                username=f"test{cook_id}",
                password=f"password{cook_id}",
            )

    def test_cook_view_url_exists_at_desired_location(self):
        response = self.client.get("/cooks/")
        self.assertEqual(response.status_code, 200)

    def test_cook_view_url_accessible_by_name(self):
        response = self.client.get(COOK_URL)
        self.assertEqual(response.status_code, 200)

    def test_cook_uses_correct_template_name(self):
        res = self.client.get(COOK_URL)
        self.assertTemplateUsed(res, "kitchen/cook_list.html")

    def test_cook_pagination_is_five(self):
        res = self.client.get(COOK_URL)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["cook_list"]), 5)
        self.assertEqual(
            list(res.context["cook_list"]),
            list(get_user_model().objects.filter(pk__lte=5))
        )

    def test_lists_all_dishes(self):
        res = self.client.get(COOK_URL + "?page=2")
        self.assertEqual(res.status_code, 200)
        self.assertTrue("is_paginated" in res.context)
        self.assertTrue(res.context["is_paginated"])
        self.assertEqual(len(res.context["cook_list"]), 2)


class CookCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.cook_create_url = reverse("kitchen:cook-create")

    def test_cook_create_view_url_exists_at_desired_location(self):
        res = self.client.get("/cooks/create/")
        self.assertEqual(res.status_code, 200)

    def test_cook_create_view_url_accessible_by_name(self):
        res = self.client.get(self.cook_create_url)
        self.assertEqual(res.status_code, 200)

    def test_cook_create_uses_correct_template_name(self):
        res = self.client.get(self.cook_create_url)
        self.assertTemplateUsed(res, "kitchen/cook_form.html")

    def test_cook_create(self):
        res = self.client.post(
            self.cook_create_url,
            {
                "username": "test123",
                "password1": "sdaqdsa532",
                "password2": "sdaqdsa532",
                "years_of_experience": 5
            }
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/cooks/")
        self.assertEqual(
            get_user_model().objects.get(pk=2).username,
            "test123"
        )


class CookUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            years_of_experience=5
        )
        self.client.force_login(self.user)
        self.cook_update_url = reverse(
            "kitchen:cook-update",
            args=(self.user.id,)
        )


    def test_cook_update_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/cooks/{self.user.id}/update/")
        self.assertEqual(res.status_code, 200)

    def test_cook_update_view_url_accessible_by_name(self):
        res = self.client.get(self.cook_update_url)
        self.assertEqual(res.status_code, 200)

    def test_cook_update_uses_correct_template_name(self):
        res = self.client.get(self.cook_update_url)
        self.assertTemplateUsed(res, "kitchen/cook_form.html")

    def test_cook_update(self):
        res = self.client.post(
            self.cook_update_url,
            {
                "username":"test",
                "password":"test123",
                "email": "admin@admin.com",
                "first_name": "test",
                "last_name": "test",
                "years_of_experience": 6,
            }
        )
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/cooks/")
        self.assertEqual(self.user.years_of_experience, 5)
        self.user.refresh_from_db()
        self.assertEqual(self.user.years_of_experience, 6)


class CookDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.cook = get_user_model().objects.create_user(
            username="test123",
            password="test123",
        )
        self.cook_delete_url = reverse(
            "kitchen:cook-delete",
            args=[self.cook.id]
        )

    def test_cook_delete_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/cooks/{self.cook.id}/delete/")
        self.assertEqual(res.status_code, 200)

    def test_cook_delete_view_url_accessible_by_name(self):
        res = self.client.get(self.cook_delete_url)
        self.assertEqual(res.status_code, 200)

    def test_cook_delete_uses_correct_template_name(self):
        res = self.client.get(self.cook_delete_url)
        self.assertTemplateUsed(res, "kitchen/cook_delete_confirm.html")

    def test_cook_delete(self):
        res = self.client.post(self.cook_delete_url)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/cooks/")
        self.assertFalse(get_user_model().objects.filter(id=self.cook.id))


class CookDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.cook_detail_url = reverse("kitchen:cook-detail", args=[self.user.id])

    def test_cook_detail_view_url_exists_at_desired_location(self):
        res = self.client.get(f"/cooks/{self.user.id}/")
        self.assertEqual(res.status_code, 200)

    def test_cook_detail_view_url_accessible_by_name(self):
        res = self.client.get(self.cook_detail_url)
        self.assertEqual(res.status_code, 200)

    def test_cook_detail_uses_correct_template_name(self):
        res = self.client.get(self.cook_detail_url)
        self.assertTemplateUsed(res, "kitchen/cook_detail.html")
