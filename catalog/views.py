from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    TemplateView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import ProductForm
from .models import Product


class HomeView(ListView):
    """Главная страница: список продуктов"""
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"


class ContactView(TemplateView):
    """Страница контактов"""
    template_name = "catalog/contacts.html"


class ProductDetailView(DetailView):
    """Детали продукта"""
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание продукта. Только для авторизованных."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")
    login_url = "/accounts/login/"
    redirect_field_name = "redirect_to"


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта. Только для авторизованных."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")
    login_url = "/accounts/login/"
    redirect_field_name = "redirect_to"


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление продукта. Только для авторизованных."""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")
    login_url = "/accounts/login/"
    redirect_field_name = "redirect_to"
