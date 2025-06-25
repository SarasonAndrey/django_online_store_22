# catalog/views.py
from django.views.generic import ListView, TemplateView, DetailView
from .models import Product

class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'  # чтобы не использовать object_list


class ContactView(TemplateView):
    template_name = 'catalog/contacts.html'  # Отображение шаблона contact.html


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


