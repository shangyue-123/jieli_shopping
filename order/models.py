from django.db import models
from user.models import user,consignee
# Create your models here.
# 定义订单信息表
class order(models.Model):
    ORDER_STATUS_ITEM = [
        (0,'待支付'),
        (1,'待发货'),
        (2,'待收货'),
        (3,'已收货'),
        (4,'换货'),
        (9,'完成换货'),
        (11,'取消换货'),
        (5,'退货'),
        (10,'完成退货'),
        (12,'取消退货'),
        (6,'订单取消中'),
        (7,'订单已取消'),
        (8,'订单已删除'),

    ]

    PAYMENT_METHOD_ITEM = [
        (0,'现金支付'),
        (1,'微信支付'),
        (2,'支付宝支付'),
    ]
    id = models.AutoField(primary_key=True)

    user= models.ForeignKey(user, verbose_name='用户信息表', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=20, verbose_name='用户名', default='NULL')

    goods_json = models.JSONField(verbose_name='商品id和数量',null=True)

    payment_amount = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='支付金额')
    payment_method = models.IntegerField(choices=PAYMENT_METHOD_ITEM,verbose_name='支付方式')
    payment_time = models.DateTimeField(verbose_name='支付时间',null=True)

    expected_time = models.DateTimeField(verbose_name='期望配送时间',null=True)

    consignee_name = models.CharField(max_length=20, verbose_name='收件人姓名',default='NULL')
    consignee_number = models.CharField(max_length=11, verbose_name='收件人手机号',default='NULL')
    consignee_address = models.CharField(max_length=100, verbose_name='收货地址',default='NULL')

    order_status = models.IntegerField(choices=ORDER_STATUS_ITEM,verbose_name='订单状态')
    order_time = models.DateTimeField(auto_now_add=True,verbose_name='订单创建时间')

    # integral_use = models.BooleanField(verbose_name='是否使用积分',default=False)
    integral_number = models.IntegerField(verbose_name='积分数量',default=0)