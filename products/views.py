# views.py
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Product, Category
from .forms import ProductFilterForm
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().filter(available=True)
        form = ProductFilterForm(self.request.GET)
        
        if form.is_valid():
            data = form.cleaned_data
            if data['search']:
                queryset = queryset.filter(
                    Q(name__icontains=data['search']) |
                    Q(description__icontains=data['search'])
                )
            if data['category']:
                category = data['category']
                queryset = queryset.filter(category=category)
            if data['min_price']:
                queryset = queryset.filter(price__gte=data['min_price'])
            if data['max_price']:
                queryset = queryset.filter(price__lte=data['max_price'])
            if data['min_rating']:
                queryset = queryset.filter(rating__gte=data['min_rating'])
        
        return queryset.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = ProductFilterForm(self.request.GET)
        context['categories'] = Category.objects.filter(parent=None)
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        return get_object_or_404(Product, id=self.kwargs['product_id'])


class CategoryProductListView(ProductListView):
    def get_queryset(self):
        category_slug = self.kwargs['slug']
        category = Category.objects.get(slug=category_slug)
        return super().get_queryset().filter(category=category)