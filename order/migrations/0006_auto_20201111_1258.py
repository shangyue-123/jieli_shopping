# Generated by Django 3.1.2 on 2020-11-11 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20201106_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='支付金额'),
        ),
    ]