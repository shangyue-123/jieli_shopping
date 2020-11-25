# Generated by Django 3.1 on 2020-09-28 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20200926_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.IntegerField(choices=[(0, '待支付'), (1, '待发货'), (2, '待收货'), (3, '已收货'), (4, '换货'), (5, '退货'), (6, '订单取消中'), (7, '订单已取消'), (8, '订单已删除')], verbose_name='订单状态'),
        ),
    ]