from catalog.models import Product


def get_products_by_category(category_id):
    """
    Возвращает все продукты в указанной категории.
    """
    return Product.objects.filter(category_id=category_id).select_related("category")
