# Generated by Django 3.1.2 on 2020-11-11 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discounts', '0003_auto_20201109_1042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='integral',
            old_name='integral_number',
            new_name='number',
        ),
        migrations.AddField(
            model_name='integral',
            name='change',
            field=models.IntegerField(default=0, verbose_name='积分增减'),
        ),
        migrations.AddField(
            model_name='integral',
            name='change_reason',
            field=models.IntegerField(choices=[(0, '推荐新用户'), (1, '推荐用户消费'), (2, '购买商品获取'), (3, '活动获取'), (4, '新用户注册'), (6, '购买商品消费'), (11, '不变化')], default=11, verbose_name='积分变化原因'),
        ),
    ]