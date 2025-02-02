from django.test import TestCase
from django.urls import reverse
from .models import Product, Category
from django.utils.text import slugify
from django.contrib.auth.models import User
from orders.models import Order

class OrderModelTest(TestCase):
    def setUp(self):
        # Create a user for the order
        self.user = User.objects.create_user(username='testuser', password='password')
        self.order = Order.objects.create(
            user=self.user,
            # other required fields for Order
        )


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', description='Electronic items')

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertTrue(self.category.slug)  # Ensure that the slug is created automatically

    def test_category_slug_generation(self):
        slug = slugify(self.category.name)
        self.assertEqual(self.category.slug, slug)

    def test_category_absolute_url(self):
        # Test the absolute URL for the category
        url = self.category.get_absolute_url()
        self.assertEqual(url, reverse('products_by_category', args=[self.category.slug]))


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', description='Electronic items')
        self.product = Product.objects.create(
            name='Laptop',
            description='A powerful laptop',
            price=1500.00,
            category=self.category,
            stock=10,
            available=True,
            image='products/img/laptop.jpg'
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Laptop')
        self.assertTrue(self.product.slug)  # Ensure that the slug is created automatically
        self.assertEqual(self.product.category, self.category)

    def test_product_slug_generation(self):
        slug = slugify(self.product.name)
        self.assertEqual(self.product.slug, slug)

    def test_product_absolute_url(self):
        # Test the absolute URL for the product
        url = self.product.get_absolute_url()
        self.assertEqual(url, reverse('product_detail', args=[self.product.slug]))

class ProductListViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', description='Electronic items')
        Product.objects.create(
            name='Laptop',
            description='A powerful laptop',
            price=1500.00,
            category=self.category,
            stock=10,
            available=True,
            image='products/img/laptop.jpg'
        )
        Product.objects.create(
            name='Smartphone',
            description='A fast smartphone',
            price=700.00,
            category=self.category,
            stock=20,
            available=True,
            image='products/img/smartphone.jpg'
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')
        self.assertContains(response, 'Smartphone')

    def test_product_list_view_pagination(self):
        response = self.client.get(reverse('product_list') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Smartphone')

    def test_product_list_filter_by_category(self):
        response = self.client.get(reverse('product_list') + '?category=' + self.category.slug)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')
        self.assertContains(response, 'Smartphone')

    def test_product_detail_view(self):
        product = Product.objects.first()
        response = self.client.get(reverse('product_detail', args=[product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, product.name)

    def test_category_product_list_view(self):
        response = self.client.get(reverse('products_by_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')
        self.assertContains(response, 'Smartphone')

class TestUrls(TestCase):
    def test_category_product_list_url(self):
        url = reverse('products_by_category', kwargs={'slug': 'electronics'})
        self.assertEqual(url, '/products/category/electronics/')
        
    def test_product_detail_url(self):
        url = reverse('product_detail', kwargs={'slug': 'laptop'})
        self.assertEqual(url, '/products/laptop/')

    def test_product_list_url(self):
        url = reverse('product_list')
        self.assertEqual(url, '/products/')
