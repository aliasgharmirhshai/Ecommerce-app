# urls.py
from django.urls import path
from .views import ProductListView, ProductDetailView, CategoryProductListView

app_name = 'products'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('category/<slug:slug>/', CategoryProductListView.as_view(), name='products_by_category'),
    path('<int:product_id>/', ProductDetailView.as_view(), name='product_detail'),
]