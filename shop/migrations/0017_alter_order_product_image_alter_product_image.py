# Generated by Django 4.0 on 2022-01-31 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='product_image',
            field=models.ImageField(upload_to='media/shop/images'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='media/shop/images'),
        ),
    ]
