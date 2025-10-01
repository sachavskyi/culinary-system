from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

COOK_URL = reverse("kitchen:cook-list")


class CookSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="qwe",
            password="test123",
            years_of_experience=5,
        )
        get_user_model().objects.create_user(
            username="zxc",
            password="test123",
            years_of_experience=6,
        )

    def test_cook_search_without_query(self):
        res = self.client.get(COOK_URL)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "qwe")
        self.assertContains(res, "zxc")

    def test_cook_search_with_correct_query(self):
        res = self.client.get(COOK_URL, {"search": "qw"})
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "qwe")
        self.assertNotContains(res, "zxc")

    def test_cook_search_with_wrong_query(self):
        res = self.client.get(COOK_URL, {"search": "YYY"})
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "qwe")
        self.assertNotContains(res, "zxc")
