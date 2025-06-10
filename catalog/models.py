from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="наименование")
    description = models.TextField(blank=True, null=True, verbose_name="описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    models.TextField(blank=True, null=True, verbose_name='описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="изображение")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products", verbose_name="категория"
    )
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена за покупку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата последнего изменения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['name']
