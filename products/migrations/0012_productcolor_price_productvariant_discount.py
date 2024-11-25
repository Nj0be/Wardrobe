# Generated by Django 5.1.3 on 2024-11-25 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_productcolor_default_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcolor',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.discount'),
        ),
    ]