# Generated by Django 5.2.1 on 2025-06-10 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="описание"),
        ),
    ]
