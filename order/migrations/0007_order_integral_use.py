# Generated by Django 3.1.2 on 2020-11-11 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20201111_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='integral_use',
            field=models.BooleanField(default=False, verbose_name='是否使用积分'),
        ),
    ]
