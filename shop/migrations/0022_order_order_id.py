# Generated by Django 4.0 on 2022-02-02 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_contact_contact_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
