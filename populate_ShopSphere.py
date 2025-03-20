import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'shop_sphere_project.settings')

import django
django.setup()
from ShopSphere.models import Category, Page

import random
from decimal import Decimal
from ShopSphere.models import ProductCategory, Product

def populate():
    # First, we will create lists of dictionaries containing the pages
    # we want to add into each category.
    # Then we will create a dictionary of dictionaries for our categories.
    # This might seem a little bit confusing, but it allows us to iterate
    # through each data structure, and add the data to our models.
    
    python_pages = [
    {'title': 'Official Python Tutorial',
    'url':'http://docs.python.org/3/tutorial/', 'views': 7},
    {'title':'How to Think like a Computer Scientist',
    'url':'http://www.greenteapress.com/thinkpython/', 'views': 14},
    {'title':'Learn Python in 10 Minutes',
    'url':'http://www.korokithakis.net/tutorials/python/', 'views': 26} ]
    
    django_pages = [
    {'title':'Official Django Tutorial',
    'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/', 'views': 42},
    {'title':'Django Rocks',
    'url':'http://www.djangorocks.com/', 'views': 11},
    {'title':'How to Tango with Django',
    'url':'http://www.tangowithdjango.com/', 'views': 23} ]
        
    other_pages = [
    {'title':'Bottle',
    'url':'http://bottlepy.org/docs/dev/', 'views': 50},
    {'title':'Flask',
    'url':'http://flask.pocoo.org', 'views': 1002} ]
    
    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
    'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
    'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16}, }
    
    categories = create_categories()
    create_products()

    # If you want to add more categories or pages,
    # add them to the dictionaries above.
    
    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data.get("views"), likes=cat_data.get("likes"))
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    # Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=10, likes=10):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c
    

def create_categories():
   """Create some example product categories."""
   print('creating product categories')
   categories = ["Electronics", "Clothing", "Home & Kitchen", "Books", "Toys & Games"]
   category_objects = []
   for cat in categories:
       category, created = ProductCategory.objects.get_or_create(name=cat)
       category_objects.append(category)
   return category_objects

def create_products(categories):
   """Create some example products in each category."""
   print('adding products')
   product_data = {
       "Electronics": [
           {"name": "Smartphone", "description": "Latest model smartphone.", "price": 699.99, "stock": 10},
           {"name": "Laptop", "description": "Powerful gaming laptop.", "price": 1299.99, "stock": 5},
       ],
       "Clothing": [
           {"name": "T-Shirt", "description": "100% cotton, various sizes.", "price": 19.99, "stock": 50},
           {"name": "Jeans", "description": "Denim jeans for all sizes.", "price": 49.99, "stock": 30},
       ],
       "Home & Kitchen": [
           {"name": "Coffee Maker", "description": "Brews coffee in minutes.", "price": 89.99, "stock": 15},
           {"name": "Vacuum Cleaner", "description": "Cordless vacuum cleaner.", "price": 199.99, "stock": 8},
       ],
       "Books": [
           {"name": "Python Programming", "description": "Learn Python with this guide.", "price": 39.99, "stock": 20},
           {"name": "Django for Beginners", "description": "Step-by-step Django tutorial.", "price": 29.99, "stock": 25},
       ],
       "Toys & Games": [
           {"name": "LEGO Set", "description": "Creative building blocks.", "price": 59.99, "stock": 12},
           {"name": "Board Game", "description": "Fun for the whole family.", "price": 34.99, "stock": 20},
       ],
   }
   for category in categories:
       if category.name in product_data:
           for product in product_data[category.name]:
               Product.objects.get_or_create(
                   category=category,
                   name=product["name"],
                   description=product["description"],
                   price=Decimal(product["price"]),
                   stock=product["stock"]
               )

# Start execution here!
if __name__ == '__main__':
    print('Starting ShopSphere population script...')
    populate()
