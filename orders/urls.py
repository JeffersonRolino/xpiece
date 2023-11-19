from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('download/<int:id>/', views.order_items_download, name='order_download'),
    path('redirect-me/<int:id>/', views.redirect_me, name='redirect-me')
]
