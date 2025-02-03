from django.urls import path
from .views import AddToCartView, CartView

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='view_cart'),
]