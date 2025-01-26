from django.test import TestCase
from .models import Order

class OrderModelTest(TestCase):

    def setUp(self):
        self.order = Order.objects.create(
            # Add fields as per your Order model
            # Example: product=product_instance, quantity=1, user=user_instance
        )

    def test_order_creation(self):
        self.assertIsInstance(self.order, Order)

    def test_order_str(self):
        self.assertEqual(str(self.order), 'Expected string representation')  # Adjust as necessary

    # Add more tests as needed for your Order model and functionality