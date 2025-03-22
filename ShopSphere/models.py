from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.

    def __str__(self):
        return self.user.username

   
class Product(models.Model):
   category = models.CharField(max_length=255)
   name = models.CharField(max_length=255)
   description = models.TextField()
   price = models.DecimalField(max_digits=10, decimal_places=2)
   stock = models.PositiveIntegerField()
   image = models.ImageField(upload_to='product_images/', blank=True, null=True)
   def __str__(self):
       return self.name
   
#class UserProfile(models.Model):
 #  user = models.OneToOneField(User, on_delete=models.CASCADE)
  # address = models.TextField(blank=True, null=True)
   #profile_image = models.ImageField(upload_to='profile_images/', blank=True)
   #def __str__(self):
    #   return self.user.username


