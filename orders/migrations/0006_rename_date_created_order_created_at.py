# Generated by Django 5.1.3 on 2024-12-02 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_address_line_two'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='date_created',
            new_name='created_at',
        ),
    ]
