# urls.py
from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryProductListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/category/<slug:slug>/', CategoryProductListView.as_view(), name='products_by_category'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]