from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="user@example.com",
            name="John",
            last_name="Doe",
            phone_number="1234567890",
            password="securepassword123"
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("securepassword123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@example.com",
            name="Admin",
            last_name="User",
            phone_number="0987654321",
            password="securepassword123"
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_user_str(self):
        user = User.objects.create_user(
            email="test@example.com",
            name="Test",
            last_name="User",
            phone_number="1234567890",
            password="testpassword123"
        )
        self.assertEqual(str(user), "Test User (test@example.com)")

class UserRegistrationTests(TestCase):
    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            "email": "newuser@example.com",
            "name": "New",
            "last_name": "User",
            "phone_number": "1234567890",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_register_user_invalid(self):
        response = self.client.post(reverse('register'), {
            "email": "invaliduser@example.com",
            "name": "Invalid",
            "last_name": "User",
            "phone_number": "1234567890",
            "password1": "pass",
            "password2": "pass"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email="invaliduser@example.com").exists())

class UserLoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="loginuser@example.com",
            name="Login",
            last_name="User",
            phone_number="1234567890",
            password="securepassword123"
        )

    def test_login_valid_user(self):
        response = self.client.post(reverse('login'), {
            "username": "loginuser@example.com",
            "password": "securepassword123"
        })
        self.assertEqual(response.status_code, 302)

    def test_login_invalid_user(self):
        response = self.client.post(reverse('login'), {
            "username": "wronguser@example.com",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)

class UserLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="logoutuser@example.com",
            name="Logout",
            last_name="User",
            phone_number="1234567890",
            password="securepassword123"
        )
        self.client.login(username="logoutuser@example.com", password="securepassword123")

    def test_logout_user(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
