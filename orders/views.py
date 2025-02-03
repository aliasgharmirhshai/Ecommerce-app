from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
from .templatetags.cart_extras import multiply

class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"Updated quantity for {product.name} in your cart.")
        else:
            messages.success(request, f"Added {product.name} to your cart.")

        return redirect('products:product_detail', product_id=product_id)
    

class CartView(View):
    def get(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        total_price = cart.get_total_price()
        return render(request, 'orders/view_cart.html', {
            'cart_items': cart_items,
            'total_price': total_price
        })
