# Generated by Django 5.1.3 on 2024-11-20 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_productvariant_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='position',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]