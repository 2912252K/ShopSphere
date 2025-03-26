from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.admin.sites import site
from ShopSphere.models import Category, Page, Product, Cart, CartItem, UserProfile
from ShopSphere.forms import CategoryForm, PageForm, UserForm, ProductForm
from ShopSphere.admin import CategoryAdmin, PageAdmin
from ShopSphere.cart import Cart as SessionCart
from django.db.models.signals import post_save
from django.dispatch import receiver

class ShopSphereTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='TestCategory', slug='testcategory')
        self.product = Product.objects.create(name='TestProduct', description='Test Description', price=10.99, stock=10)
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    # Views Tests
    def test_index_view(self):
        response = self.client.get(reverse('ShopSphere:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ShopSphere/index.html')

    def test_about_view(self):
        response = self.client.get(reverse('ShopSphere:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ShopSphere/about.html')

    def test_product_detail_view(self):
        response = self.client.get(reverse('ShopSphere:product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ShopSphere/product_detail.html')

    def test_product_detail_invalid_id(self):
        response = self.client.get(reverse('ShopSphere:product_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

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

    def test_show_category_invalid_slug(self):
        response = self.client.get(reverse('ShopSphere:show_category', args=['non-existent']))
        self.assertEqual(response.status_code, 404)

    def test_user_authentication(self):
        login = self.client.login(username='testuser', password='password123')
        self.assertTrue(login)

        response = self.client.get(reverse('ShopSphere:logout'))
        self.assertRedirects(response, reverse('ShopSphere:index'))

    def test_login_view_get(self):
        response = self.client.get(reverse('ShopSphere:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ShopSphere/login.html')

    def test_login_view_post_success(self):
        response = self.client.post(reverse('ShopSphere:login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('ShopSphere:index'))

    def test_login_view_post_failure(self):
        response = self.client.post(reverse('ShopSphere:login'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "invalid login", status_code=200)

    def test_recommended_view_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('ShopSphere:recommended'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ShopSphere/recommended.html')

    def test_register_view(self):
        response = self.client.post(reverse('ShopSphere:register'), {
            'username': 'newuser',
            'password': 'newpassword123',
        })
        self.assertEqual(response.status_code, 200)

    def test_protected_views_redirect(self):
        response = self.client.get(reverse('ShopSphere:recommended'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('ShopSphere:add_category'))
        self.assertEqual(response.status_code, 302)

    def test_add_page_view(self):
        response = self.client.get(reverse('ShopSphere:add_page', args=[self.category.slug]))
        self.assertEqual(response.status_code, 302)

    # Model Tests
    def test_category_model(self):
        category = Category.objects.create(name='NewCategory')
        self.assertEqual(category.name, 'NewCategory')
        self.assertEqual(category.slug, 'newcategory')

    def test_product_model(self):
        product = Product.objects.create(name='NewProduct', price=5.99, stock=20)
        self.assertEqual(product.name, 'NewProduct')
        self.assertEqual(product.price, 5.99)
        self.assertEqual(product.stock, 20)

    def test_cart_model(self):
        self.assertEqual(self.cart.total_items(), 2)
        self.assertEqual(self.cart.total_price(), self.product.price * self.cart_item.quantity)

    def test_cart_item_model(self):
        self.assertEqual(self.cart_item.total_price(), self.product.price * 2)

    # Session Cart Tests
    def test_session_cart_add_and_remove(self):
        request = self.factory.get('/')
        request.session = self.client.session
        cart = SessionCart(request)
        cart.add(self.product, quantity=3)
        self.assertEqual(len(cart.cart), 1)
        cart.remove(self.product)
        self.assertEqual(len(cart.cart), 0)

    def test_session_cart_total_price_and_length(self):
        request = self.factory.get('/')
        request.session = self.client.session
        cart = SessionCart(request)
        cart.add(self.product, quantity=2)
        self.assertEqual(cart.total_price(), self.product.price * 2)
        self.assertEqual(cart.__len__(), 2)

    # Signal Test
    def test_cart_created_on_user_creation(self):
        user = User.objects.create_user(username='signaluser', password='pass123')
        self.assertTrue(Cart.objects.filter(user=user).exists())

    # Form Tests
    def test_category_form_valid(self):
        form = CategoryForm(data={'name': 'TestCategory'})
        self.assertTrue(form.is_valid())

    def test_page_form_valid(self):
        form = PageForm(data={'title': 'TestPage', 'url': 'http://example.com', 'views': 0})
        self.assertTrue(form.is_valid())

    def test_user_form_valid(self):
        form = UserForm(data={'username': 'testuser', 'email': 'test@example.com', 'password': 'securepass123'})
        self.assertTrue(form.is_valid())

    def test_product_form_valid(self):
        form = ProductForm(data={
            'category': self.category.id,
            'name': 'TestProduct',
            'description': 'A test product',
            'price': 15.99,
            'stock': 5
        })
        self.assertTrue(form.is_valid())

    def test_invalid_category_form(self):
        form = CategoryForm(data={'name': ''})
        self.assertFalse(form.is_valid())

    def test_invalid_product_form(self):
        form = ProductForm(data={'name': '', 'price': -5, 'stock': -1})
        self.assertFalse(form.is_valid())

    # Admin Tests
    def test_admin_category_registered(self):
        self.assertTrue(site.is_registered(Category))

    def test_admin_page_registered(self):
        self.assertTrue(site.is_registered(Page))

    def test_admin_user_profile_registered(self):
        self.assertTrue(site.is_registered(UserProfile))
