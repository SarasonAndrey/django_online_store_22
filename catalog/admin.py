from django.contrib import admin
from .models import Category, Product

# Настройка отображения для модели Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Поля, которые будут отображаться в списке

# Настройка отображения для модели Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'purchase_price', 'category')  # Поля, которые будут отображаться в списке
    list_filter = ('category',)  # Фильтрация по категории
    search_fields = ('name', 'description')  # Поиск по полям name и description

# Регистрация моделей
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
