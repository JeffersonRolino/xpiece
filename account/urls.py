from django.urls import include, path

from . import views

urlpatterns = [
    # Este include() adiciona todos os paths padrões para autenticação.
    # https://docs.djangoproject.com/en/4.2/topics/auth/default/
    path('', include("django.contrib.auth.urls")),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
]
