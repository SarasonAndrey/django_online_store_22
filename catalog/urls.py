# catalog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Маршрут для домашней страницы
    path('contacts/', views.contact, name='contacts'),  # Маршрут для страницы контактов
    path('product/<int:pk>/', views.product_detail, name='product_detail'), # Маршрут для описание товаров

]
