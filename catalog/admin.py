from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    """Категории: отображение ID и названия."""

    list_display = ("id", "name")


class ProductAdmin(admin.ModelAdmin):
    """Продукты: список (ID, название, цена, категория), фильтр по категории, поиск по имени и описанию."""

    list_display = ("id", "name", "purchase_price", "category")
    list_filter = ("category",)
    search_fields = ("name", "description")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
