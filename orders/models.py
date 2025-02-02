from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ordered_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(max_length=255)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"