# Generated by Django 4.0 on 2022-02-01 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_category_sub_category_alter_product_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='subcategory',
        ),
        migrations.DeleteModel(
            name='Sub_Category',
        ),
    ]
