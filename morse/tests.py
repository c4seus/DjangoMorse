from django.test import TestCase
from django.urls import reverse

class SimpleTest(TestCase):
    def test_homepage_status_code(self):
        response = self.client.get(reverse("home_view"))
        self.assertEqual(response.status_code, 200)