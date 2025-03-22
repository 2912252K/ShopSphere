from django.urls import path
from ShopSphere import views
from shop_sphere_project import settings
from django.conf.urls.static import static

app_name = 'ShopSphere'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'), 
    path('recommended/', views.recommended, name='recommended'),
    path('logout/', views.user_logout, name='logout'),
    
    path('product/<int:product_id>/', views.product_detail, name='product_detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
