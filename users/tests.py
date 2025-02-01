from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model

@override_settings(LOGIN_URL='/users/login/')
class UserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            phone_number="1234567890",
            password="testpassword123",
            name="Test",
            last_name="User"
        )
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.dashboard_url = reverse("dashboard")

    def test_login_with_email(self):
        response = self.client.post(self.login_url, {
            "username": "testuser@example.com",
            "password": "testpassword123"
        })
        self.assertRedirects(response, self.dashboard_url)

    def test_login_with_phone_number(self):
        response = self.client.post(self.login_url, {
            "username": "1234567890",
            "password": "testpassword123"
        })
        self.assertRedirects(response, self.dashboard_url)

    def test_dashboard_access_authenticated(self):
        self.client.login(email="testuser@example.com", password="testpassword123")
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_access_unauthenticated(self):
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, f"{self.login_url}?next={self.dashboard_url}")

    def test_logout(self):
        self.client.login(email="testuser@example.com", password="testpassword123")
        self.client.get(self.logout_url)
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, f"{self.login_url}?next={self.dashboard_url}")
