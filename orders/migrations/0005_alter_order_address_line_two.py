# Generated by Django 5.1.3 on 2024-11-21 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_product_variant_orderproduct_variant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address_line_two',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Riga Indirizzo 2'),
        ),
    ]
