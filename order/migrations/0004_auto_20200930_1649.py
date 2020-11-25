# Generated by Django 3.1 on 2020-09-30 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20200928_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='consignee_address',
            field=models.CharField(default='NULL', max_length=100, verbose_name='收货地址'),
        ),
        migrations.AddField(
            model_name='order',
            name='consignee_name',
            field=models.CharField(default='NULL', max_length=20, verbose_name='收件人姓名'),
        ),
        migrations.AddField(
            model_name='order',
            name='consignee_number',
            field=models.CharField(default='NULL', max_length=11, verbose_name='收件人手机号'),
        ),
        migrations.AddField(
            model_name='order',
            name='user_name',
            field=models.CharField(default='NULL', max_length=20, verbose_name='用户名'),
        ),
    ]