# Generated by Django 3.1 on 2020-09-22 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200921_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='goods_list',
        ),
        migrations.AddField(
            model_name='order',
            name='goods_json',
            field=models.JSONField(null=True, verbose_name='商品id和数量'),
        ),
    ]