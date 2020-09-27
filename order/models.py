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
        (5,'退货'),
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
    consignee= models.ForeignKey(consignee,verbose_name='收货信息表',on_delete=models.CASCADE)
    # goods = models.ForeignKey(goods,verbose_name='商品信息表',on_delete=models.CASCADE)
    user= models.ForeignKey(user, verbose_name='用户信息表', on_delete=models.CASCADE)
    # goods_list = models.CharField(max_length=1024,verbose_name='商品列表',default='null')
    goods_json = models.JSONField(verbose_name='商品id和数量',null=True)
    order_status = models.IntegerField(choices=ORDER_STATUS_ITEM,verbose_name='订单状态')
    order_time = models.DateTimeField(auto_now_add=True,verbose_name='订单创建时间')
    payment_amount = models.FloatField(verbose_name='支付金额')
    payment_method = models.IntegerField(choices=PAYMENT_METHOD_ITEM,verbose_name='支付方式')
    payment_time = models.DateTimeField(verbose_name='支付时间',null=True)
    expected_time = models.DateTimeField(verbose_name='期望配送时间',null=True)