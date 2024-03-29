# Generated by Django 3.1 on 2020-08-20 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_state',
            field=models.IntegerField(choices=[(0, '注销'), (1, '正常'), (2, '冻结')], default=1, verbose_name='用户状态'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_gender',
            field=models.IntegerField(choices=[(0, '男'), (1, '女')], verbose_name='性别'),
        ),
    ]
