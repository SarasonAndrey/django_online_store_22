from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    """Загружает тестовые данные: удаляет старые, создаёт категории и товары."""

    def handle(self, *args, **kwargs):
        """Основной метод команды: очистка и заполнение тестовыми данными."""
        self.stdout.write("Удаление всех существующих категорий и продуктов...")
        Category.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write("Создание тестовых категорий...")
        electronics = Category.objects.create(
            name="Electronics", description="Devices and gadgets"
        )
        books = Category.objects.create(
            name="Books", description="Literature and educational materials"
        )

        self.stdout.write("Создание тестовых продуктов...")
        Product.objects.create(
            name="Laptop",
            description="A high-performance laptop.",
            category=electronics,
            purchase_price=1500.00,
        )
        Product.objects.create(
            name="Python Programming",
            description="A book about Python programming.",
            category=books,
            purchase_price=30.00,
        )

        self.stdout.write(self.style.SUCCESS("✅ Тестовые продукты успешно добавлены!"))
