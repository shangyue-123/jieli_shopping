# Generated by Django 3.1.2 on 2020-11-17 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_user_referrer'),
    ]

    operations = [
        migrations.CreateModel(
            name='invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8, verbose_name='邀请码')),
                ('qr', models.ImageField(upload_to='user_QR/', verbose_name='二维码储存地址')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.user', verbose_name='用户信息表')),
            ],
        ),
    ]
