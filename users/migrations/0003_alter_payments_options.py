# Generated by Django 5.1.4 on 2025-01-06 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_payments"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="payments",
            options={
                "ordering": ("-way_pay",),
                "verbose_name": "Платеж",
                "verbose_name_plural": "Платежи",
            },
        ),
    ]
