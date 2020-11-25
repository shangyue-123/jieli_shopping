from django.db import models
from goods.models import goods
from user.models import user
# Create your models here.
# 商品特价
class goods_special(models.Model):
    GOODS_PREFERENTIAL = [
        (0, '无优惠'),
        (1, '特价优惠'),
    ]
    goods = models.OneToOneField(goods,verbose_name='商品信息外键',on_delete=models.CASCADE)
    preferential_price = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='特价',blank=False)
    goods_preferential = models.IntegerField(choices=GOODS_PREFERENTIAL,verbose_name='优惠方式',default=0)



class integral(models.Model):
    CHANGE_REASON = [
        (0,'推荐新用户'),
        (1,'推荐用户消费'),
        (2,'购买商品获取'),
        (3,'活动获取'),
        (4,'新用户注册'),
        (6,'购买商品消费'),
        (7,'退换货扣除积分'),
        (11,'不变化'),

    ]
    user = models.ForeignKey(user,on_delete=models.CASCADE,verbose_name='用户信息表')
    change_reason = models.IntegerField(choices=CHANGE_REASON,verbose_name='积分变化原因',default=11)
    change = models.IntegerField(verbose_name='积分增减',default=0)
    number = models.PositiveIntegerField(verbose_name='积分',default=0)
    date = models.DateField(auto_now_add=True,verbose_name='积分增减时间',null=True)
