# Generated by Django 4.0 on 2022-02-02 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='shop/images'),
        ),
    ]
