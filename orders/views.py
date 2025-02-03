from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
from django.http import JsonResponse
from .templatetags.cart_extras import multiply
import json

class CartView(View):
    def get(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        total_price = cart.get_total_price()
        return render(request, 'orders/view_cart.html', {
            'cart_items': cart_items,
            'total_price': total_price
        })

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
    
class UpdateCartView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            action = data.get('action')
            cart = self._get_cart(request)

            if not cart:
                return JsonResponse({'status': 'error', 'message': 'Cart not found'}, status=400)

            try:
                cart_item = CartItem.objects.get(id=item_id, cart=cart)

                if action == 'update':
                    quantity = int(data.get('quantity', 1))
                    if quantity > 0:
                        cart_item.quantity = quantity
                        cart_item.save()
                    else:
                        cart_item.delete()
                elif action == 'remove':
                    cart_item.delete()

                return JsonResponse({
                    'status': 'success',
                    'cart_total': cart.get_total_price(),
                    'new_total': cart_item.get_total_price() if action == 'update' else 0
                })
            except CartItem.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    def _get_cart(self, request):
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
        return cart


class SaveCartView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            session_cart = self._get_cart(request, guest=True)
            user_cart, _ = Cart.objects.get_or_create(user=request.user)

            for item in session_cart.items.all():
                user_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
                if not created:
                    user_item.quantity += item.quantity
                    user_item.save()

            session_cart.delete()
            return JsonResponse({'status': 'success', 'message': 'Cart saved successfully'})
        return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)

    def _get_cart(self, request, guest=False):
        if guest:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
            return cart
        return Cart.objects.filter(user=request.user).first()
