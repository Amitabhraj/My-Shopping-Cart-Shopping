# Generated by Django 4.0 on 2022-09-13 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_order_transaction_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bulk_Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=250, null=True)),
                ('main_body', models.CharField(blank=True, max_length=550, null=True)),
                ('send_to', models.CharField(blank=True, max_length=250, null=True)),
                ('attachment', models.FileField(blank=True, max_length=1000000, null=True, upload_to='shop/bulk_email_file')),
            ],
        ),
        migrations.CreateModel(
            name='Register_Attempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, default='XXXXXXX', max_length=200, null=True)),
                ('password', models.CharField(blank=True, default='XXXXXXX', max_length=200, null=True)),
                ('email', models.CharField(blank=True, default='XXXXXXX', max_length=200, null=True)),
                ('phone_number', models.IntegerField(blank=True, default=0, null=True)),
                ('otp', models.IntegerField(blank=True, default=0, null=True)),
                ('successfully_register', models.BooleanField(default=False)),
            ],
        ),
    ]
