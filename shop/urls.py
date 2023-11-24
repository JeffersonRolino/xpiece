from django.urls import path

from .views import about, contact, product_detail, product_list

app_name = 'shop'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('<int:id>/<slug:slug>/', product_detail, name='product_detail'),
    path('<slug:category_slug>/', product_list, name='product_list_by_category'),
]
