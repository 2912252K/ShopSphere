from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.admin.sites import site
from ShopSphere.models import Category, Page, Product, Cart, CartItem, UserProfile
from ShopSphere.forms import CategoryForm, PageForm, UserForm, ProductForm
from ShopSphere.admin import CategoryAdmin, PageAdmin

class ShopSphereTests(TestCase):
    def setUp(self):
        # Set up test data before each test runs
        self.client = Client()
        self.category = Category.objects.create(name='TestCategory', slug='testcategory')
        self.product = Product.objects.create(name='TestProduct', description='Test Description', price=10.99, stock=10)
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    # Views Tests
    def test_index_view(self):
        # Test if the index view returns a 200 response and uses the correct template
        response = self.client.get(reverse('ShopSphere:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ShopSphere/index.html')

    def test_product_detail_view(self):
        # Test if the product detail page returns a 200 response and uses the correct template
        response = self.client.get(reverse('ShopSphere:product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ShopSphere/product_detail.html')

    def test_cart_operations(self):
        # Test cart detail page response
        response = self.client.get(reverse('ShopSphere:cart_detail'))
        self.assertEqual(response.status_code, 200)

        # Test adding an item to the cart
        response = self.client.post(reverse('ShopSphere:add_to_cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('ShopSphere:cart_detail'))

        # Test removing an item from the cart
        response = self.client.post(reverse('ShopSphere:remove_from_cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('ShopSphere:cart_detail'))

        # Test clearing the cart
        response = self.client.post(reverse('ShopSphere:clear_cart'))
        self.assertRedirects(response, reverse('ShopSphere:cart_detail'))

    def test_category_view(self):
        # Test if the category view returns a 200 response and uses the correct template
        response = self.client.get(reverse('ShopSphere:show_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ShopSphere/category.html')

    def test_user_authentication(self):
        # Test user login
        login = self.client.login(username='testuser', password='password123')
        self.assertTrue(login)

        # Test user logout
        response = self.client.get(reverse('ShopSphere:logout'))
        self.assertRedirects(response, reverse('ShopSphere:index'))

    def test_register_view(self):
        # Test the registration process
        response = self.client.post(reverse('ShopSphere:register'), {
            'username': 'newuser',
            'password': 'newpassword123',
        })
        self.assertEqual(response.status_code, 200)

    def test_protected_views_redirect(self):
        # Test if protected views redirect to login when accessed anonymously
        response = self.client.get(reverse('ShopSphere:recommended'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('ShopSphere:add_category'))
        self.assertEqual(response.status_code, 302)

    def test_add_page_view(self):
        # Test if adding a page redirects to login if user is not authenticated
        response = self.client.get(reverse('ShopSphere:add_page', args=[self.category.slug]))
        self.assertEqual(response.status_code, 302)

    # Model Tests
    def test_category_model(self):
        # Test category model creation and slug generation
        category = Category.objects.create(name='NewCategory')
        self.assertEqual(category.name, 'NewCategory')
        self.assertEqual(category.slug, 'newcategory')

    def test_product_model(self):
        # Test product model creation and field values
        product = Product.objects.create(name='NewProduct', price=5.99, stock=20)
        self.assertEqual(product.name, 'NewProduct')
        self.assertEqual(product.price, 5.99)
        self.assertEqual(product.stock, 20)

    def test_cart_model(self):
        # Test cart model's total item count and total price calculation
        self.assertEqual(self.cart.total_items(), 2)
        self.assertEqual(self.cart.total_price(), self.product.price * self.cart_item.quantity)

    def test_cart_item_model(self):
        # Test cart item model's total price calculation
        self.assertEqual(self.cart_item.total_price(), self.product.price * 2)

    # Form Tests
    def test_category_form_valid(self):
        # Test if the category form is valid with correct data
        form = CategoryForm(data={'name': 'TestCategory'})
        self.assertTrue(form.is_valid())

    def test_page_form_valid(self):
        # Test if the page form is valid with correct data
        form = PageForm(data={'title': 'TestPage', 'url': 'http://example.com', 'views': 0})
        self.assertTrue(form.is_valid())

    def test_user_form_valid(self):
        # Test if the user registration form is valid with correct data
        form = UserForm(data={'username': 'testuser', 'email': 'test@example.com', 'password': 'securepass123'})
        self.assertTrue(form.is_valid())

    def test_product_form_valid(self):
        # Test if the product form is valid with correct data
        form = ProductForm(data={'category': 'TestCategory', 'name': 'TestProduct', 'description': 'A test product', 'price': 15.99, 'stock': 5})
        self.assertTrue(form.is_valid())

    # Admin Tests
    def test_admin_category_registered(self):
        # Test if the Category model is registered in the Django admin
        self.assertTrue(site.is_registered(Category))

    def test_admin_page_registered(self):
        # Test if the Page model is registered in the Django admin
        self.assertTrue(site.is_registered(Page))

    def test_admin_user_profile_registered(self):
        # Test if the UserProfile model is registered in the Django admin
        self.assertTrue(site.is_registered(UserProfile))
