# Generated by Django 3.1.7 on 2021-12-03 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20211203_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='price_of_the_product',
            field=models.CharField(default='0', max_length=100000000),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]
