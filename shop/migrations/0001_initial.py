# Generated by Django 3.2.7 on 2021-10-10 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_p', models.ImageField(upload_to='shop/images')),
                ('cart_id', models.IntegerField(default=0)),
                ('name_p', models.CharField(max_length=200)),
                ('price_p', models.IntegerField(default='')),
                ('product_id', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=1)),
                ('user_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(default='', max_length=50)),
                ('des', models.CharField(default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_image', models.ImageField(upload_to='shop/images')),
                ('product_name', models.CharField(max_length=200)),
                ('product_price', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(default='', max_length=50)),
                ('address1', models.CharField(default='', max_length=100)),
                ('address2', models.CharField(default='', max_length=400)),
                ('city', models.CharField(default='', max_length=100)),
                ('state', models.CharField(default='', max_length=50)),
                ('zip', models.IntegerField(default=0)),
                ('phone', models.CharField(default='0', max_length=10)),
                ('order_method', models.CharField(default='', max_length=50)),
                ('product_id', models.CharField(default=0, max_length=1)),
                ('admin_id', models.IntegerField(default='')),
                ('user_uid', models.IntegerField(default=0)),
                ('order_status', models.CharField(default='Pending', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=150)),
                ('category', models.CharField(default='', max_length=30)),
                ('subcategory', models.CharField(default='', max_length=50)),
                ('price', models.CharField(default='0', max_length=10)),
                ('des', models.CharField(max_length=10000)),
                ('admin_id', models.IntegerField(default='')),
                ('image', models.ImageField(upload_to='shop/images')),
            ],
        ),
    ]
