# Generated by Django 5.1.2 on 2024-10-18 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_alter_category_options_category_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='position',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
