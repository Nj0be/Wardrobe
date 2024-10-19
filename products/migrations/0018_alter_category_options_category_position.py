# Generated by Django 5.1.2 on 2024-10-18 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_alter_category_options_remove_category_position'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['position'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='position',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
    ]
