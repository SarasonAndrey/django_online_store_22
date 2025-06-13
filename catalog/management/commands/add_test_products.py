from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Добавляет тестовые продукты в базу данных после удаления всех существующих данных.'

    def handle(self, *args, **kwargs):
        # Удаление всех существующих данных
        self.stdout.write("Удаление всех существующих категорий и продуктов...")
        Category.objects.all().delete()
        Product.objects.all().delete()

        # Создание тестовых категорий
        self.stdout.write("Создание тестовых категорий...")
        category1 = Category.objects.create(name="Electronics", description="Devices and gadgets")
        category2 = Category.objects.create(name="Books", description="Literature and educational materials")

        # Создание тестовых продуктов
        self.stdout.write("Создание тестовых продуктов...")
        Product.objects.create(
            name="Laptop",
            description="A high-performance laptop.",
            category=category1,
            purchase_price=1500.00
        )
        Product.objects.create(
            name="Python Programming",
            description="A book about Python programming.",
            category=category2,
            purchase_price=30.00
        )

        # Вывод сообщения об успешном завершении
        self.stdout.write(self.style.SUCCESS("Тестовые продукты успешно добавлены!"))