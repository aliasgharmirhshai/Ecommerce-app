from django.urls import path
from .views import AddToCartView, CartView, UpdateCartView, SaveCartView

app_name = 'orders'

urlpatterns = [
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='view_cart'),
    path('update-cart/', UpdateCartView.as_view(), name='update_cart'),
    path('save-cart/', SaveCartView.as_view(), name='save_cart'),
]