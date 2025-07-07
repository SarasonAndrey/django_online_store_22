# catalog/forms.py
from django import forms
from .models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    """Форма продукта с валидацией и стилизацией."""

    subscribe = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        """Связь с моделью и поля формы."""

        model = Product
        fields = ["name", "description", "image", "category", "purchase_price"]
        labels = {
            "name": "Название продукта",
            "description": "Описание",
            "image": "Изображение товара",
            "category": "Категория",
            "purchase_price": "Цена",
        }

    def __init__(self, *args, **kwargs):
        """Добавляет стили ко всем полям формы."""
        super(ProductForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if (
                field_name != "subscribe"
                and field.widget.__class__.__name__ != "HiddenInput"
            ):
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = f"Введите {field.label.lower()}"

        if "description" in self.fields:
            self.fields["description"].widget.attrs.update(
                {
                    "rows": 5,
                    "class": "form-control",
                    "placeholder": "Введите описание продукта",
                }
            )

        if "purchase_price" in self.fields:
            self.fields["purchase_price"].widget.attrs.update(
                {"placeholder": "Укажите цену, например: 999.99"}
            )

    def clean_name(self):
        """Проверяет название на запрещённые слова."""
        name = self.cleaned_data.get("name")
        if any(word in name.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError("Название содержит запрещённые слова.")
        return name

    def clean_description(self):
        """Проверяет описание на наличие запрещённых слов."""
        description = self.cleaned_data.get("description")
        if description and any(word in description.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError("Описание содержит запрещённые слова.")
        return description

    def clean_purchase_price(self):
        """Проверяет, что цена не отрицательная."""
        price = self.cleaned_data.get("purchase_price")
        if price is None:
            raise forms.ValidationError("Это обязательное поле.")
        if price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_subscribe(self):
        """Honeypot: если поле заполнено — запрос от бота."""
        data = self.cleaned_data.get("subscribe")
        if data:
            raise forms.ValidationError("Ошибка проверки.")
        return data
