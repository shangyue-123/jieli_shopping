from django.db import models

# from  cart.models import cart

# Create your models here.
# 定义用户信息表
from goods.models import goods


class user(models.Model):
    GENDER_ITEM = [
        (0, '男'),
        (1, '女'),
    ]

    STATE_ITEM = [
        (0, '注销'),
        (1, '正常'),
        (2, '冻结'),
    ]

    user_name = models.CharField(max_length=20, verbose_name='用户名', unique=True)
    user_password = models.CharField(max_length=256, verbose_name='密码')
    user_gender = models.IntegerField(choices=GENDER_ITEM, verbose_name='性别')
    user_number = models.CharField(max_length=11, verbose_name='手机号', blank=True)
    user_email = models.EmailField(verbose_name='邮箱', unique=True)
    user_creat_time = models.DateField(auto_now_add=True, verbose_name='用户创建时间')
    user_state = models.IntegerField(choices=STATE_ITEM, verbose_name='用户状态',default=1)


# 定义收货信息表
class consignee(models.Model):
    user = models.ForeignKey(user, verbose_name='用户信息表', on_delete=models.CASCADE)
    consignee_name = models.CharField(max_length=20, verbose_name='收件人姓名')
    consignee_number = models.CharField(max_length=11, verbose_name='收件人手机号')
    consignee_address = models.CharField(max_length=100, verbose_name='收货地址')
    consignee_default = models.BooleanField(default=0)




# class



