# catalog/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from .forms import ProductForm
from .models import Category, Product
from .services.product_service import get_products_by_category


class HomeView(ListView):
    """Главная страница с кэшированием списка опубликованных продуктов."""
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        cache_key = "published_products"
        products = cache.get(cache_key)
        if products is None:
            products = list(
                Product.objects.filter(is_published=True)
                .select_related("category", "owner")
            )
            cache.set(cache_key, products, 60 * 15)  # 15 минут
        return products


class ContactView(TemplateView):
    """Страница контактов"""
    template_name = "catalog/contacts.html"


class ProductDetailView(DetailView):
    """Детали продукта с кэшированием."""
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        cache_key = f"product_{obj.pk}"
        cached = cache.get(cache_key)
        if cached is None:
            cache.set(cache_key, obj, 60 * 15)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_moderator"] = self.request.user.has_perm("catalog.can_unpublish_product")
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_published = True
        response = super().form_valid(form)
        cache.delete("published_products")
        return response


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара. Сбрасывает кеш."""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if product.owner != request.user:
            raise PermissionDenied("Вы не можете редактировать этот товар")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        cache.delete("published_products")
        return response


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара: владелец или модератор."""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        product = self.get_object()
        if (
            product.owner != request.user
            and not request.user.groups.filter(name="Модератор продуктов").exists()
        ):
            raise PermissionDenied("У вас нет прав на удаление")
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        cache.delete("published_products")
        return response


class ProductUnpublishView(UpdateView):
    """Отмена публикации. Сбрасывает кеш."""
    model = Product
    fields = ["is_published"]
    template_name = "catalog/product_unpublish.html"
    success_url = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm("catalog.can_unpublish_product"):
            raise PermissionDenied("Нет прав")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.is_published = False
        response = super().form_valid(form)
        cache.delete(f"product_{self.object.pk}")
        cache.delete("published_products")
        return response


class ProductsByCategoryView(ListView):
    """Отображает все товары в указанной категории."""
    model = Product
    template_name = "catalog/products_by_category.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs["pk"])
        return get_products_by_category(self.category.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context
