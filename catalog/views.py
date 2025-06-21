# catalog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Product

from django.shortcuts import render


def home(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})  # Отображение шаблона home.html


def contact(request):
    return render(request, 'catalog/contacts.html')  # Отображение шаблона contact.html


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


