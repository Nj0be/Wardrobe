# Generated by Django 5.1.3 on 2024-11-24 10:08

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_productvariant_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
