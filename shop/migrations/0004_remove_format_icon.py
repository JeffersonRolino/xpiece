# Generated by Django 4.2.6 on 2023-11-11 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='format',
            name='icon',
        ),
    ]
