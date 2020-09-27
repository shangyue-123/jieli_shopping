from django.db import models
from user.models import user
from goods.models import *


# Create your models here.

class cart(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE, verbose_name='用户主键')
    goods = models.ForeignKey(goods, on_delete=models.CASCADE, verbose_name='商品主键')
    cart_goods_quantity = models.IntegerField(verbose_name='商品数量')
