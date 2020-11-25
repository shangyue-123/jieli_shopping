from django.db import models

# from  cart.models import cart

# Create your models here.
# 定义用户信息表
from goods.models import goods

#用户信息表
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

    USER_SUPER = [
        (0,'普通用户'),
        (1,'后台管理用户')
    ]

    user_name = models.CharField(max_length=20, verbose_name='用户名', unique=True)
    user_password = models.CharField(max_length=256, verbose_name='密码')
    user_gender = models.IntegerField(choices=GENDER_ITEM, verbose_name='性别')
    user_number = models.CharField(max_length=11, verbose_name='手机号', blank=True)
    user_email = models.EmailField(verbose_name='邮箱', unique=True)
    user_creat_time = models.DateField(auto_now_add=True, verbose_name='用户创建时间')
    user_state = models.IntegerField(choices=STATE_ITEM, verbose_name='用户状态',default=1)
    user_super = models.IntegerField(choices=USER_SUPER,verbose_name='是否为后台管理用户',default=0)
    user_referrer = models.IntegerField(null=True,verbose_name='推荐人id')


# 定义收货信息表
class consignee(models.Model):
    user = models.ForeignKey(user, verbose_name='用户信息表', on_delete=models.CASCADE)
    consignee_name = models.CharField(max_length=20, verbose_name='收件人姓名')
    consignee_number = models.CharField(max_length=11, verbose_name='收件人手机号')
    consignee_address = models.CharField(max_length=100, verbose_name='收货地址')
    consignee_default = models.BooleanField(default=0)


# 定义推荐二维码表
class invite(models.Model):
    user = models.OneToOneField(user,verbose_name='用户信息表',on_delete=models.CASCADE)
    code = models.CharField(max_length=8,verbose_name='邀请码',unique=True)
    qr = models.ImageField(upload_to='user_QR/',verbose_name='二维码储存地址',unique=True)



