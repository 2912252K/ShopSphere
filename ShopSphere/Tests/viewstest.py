from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ShopSphere.models import Category, Page, Product, Cart

class ShopSphereTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='TestCategory', slug='testcategory')
        self.product = Product.objects.create(name='TestProduct', price=10.99)
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_index_view(self):
        response = self.client.get(reverse('ShopSphere:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ShopSphere/index.html')

    def test_product_detail_view(self):
        response = self.client.get(reverse('ShopSphere:product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ShopSphere/product_detail.html')

    def test_cart_operations(self):
        response = self.client.get(reverse('ShopSphere:cart_detail'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('ShopSphere:add_to_cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('ShopSphere:cart_detail'))

        response = self.client.post(reverse('ShopSphere:remove_from_cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('ShopSphere:cart_detail'))

        response = self.client.post(reverse('ShopSphere:clear_cart'))
        self.assertRedirects(response, reverse('ShopSphere:cart_detail'))

    def test_category_view(self):
        response = self.client.get(reverse('ShopSphere:show_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ShopSphere/category.html')

    def test_user_authentication(self):
        login = self.client.login(username='testuser', password='password123')
        self.assertTrue(login)

        response = self.client.get(reverse('ShopSphere:user_logout'))
        self.assertRedirects(response, reverse('ShopSphere:index'))

    def test_register_view(self):
        response = self.client.post(reverse('ShopSphere:register'), {
            'username': 'newuser',
            'password': 'newpassword123',
        })
        self.assertEqual(response.status_code, 200)

    def test_protected_views_redirect(self):
        response = self.client.get(reverse('ShopSphere:recommended'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

        response = self.client.get(reverse('ShopSphere:add_category'))
        self.assertEqual(response.status_code, 302)  # Redirects to login
