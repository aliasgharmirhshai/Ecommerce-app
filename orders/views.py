from django.shortcuts import render
from django.http import HttpResponse
from .models import Order

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})

def create_order(request):
    if request.method == 'POST':
        # Logic to create an order
        return HttpResponse("Order created!")
    return render(request, 'orders/create_order.html')

def update_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        # Logic to update the order
        return HttpResponse("Order updated!")
    return render(request, 'orders/update_order.html', {'order': order})

def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    return HttpResponse("Order deleted!")