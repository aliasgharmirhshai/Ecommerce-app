from django.test import TestCase
from .models import User  # Adjust the import based on your user model

class UserModelTests(TestCase):

    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass'))

    def test_user_str(self):
        user = User(username='testuser')
        self.assertEqual(str(user), 'testuser')

    # Add more tests as needed for your user model and functionality