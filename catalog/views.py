from django.core.exceptions import PermissionDenied
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

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта. Только для авторизованных."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")
    login_url = "/accounts/login/"
    redirect_field_name = "redirect_to"


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара: владелец или модератор."""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user and not request.user.groups.filter(name="Модератор продуктов").exists():
            raise PermissionDenied("Нет прав на удаление")
        return super().dispatch(request, *args, **kwargs)


class ProductUnpublishView(UpdateView):
    """Отмена публикации. Только для модератора."""
    model = Product
    fields = ['is_published']
    template_name = "catalog/product_unpublish.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied("Нет прав")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.is_published = False
        return super().form_valid(form)
