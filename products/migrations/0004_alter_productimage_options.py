# Generated by Django 5.1.3 on 2024-11-21 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productimage_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['position']},
        ),
    ]
