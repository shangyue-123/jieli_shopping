from django.db import models

# Create your models here.
# 商品信息模块
class goods(models.Model):
    CATEGORY_ITEM = [
        (0,'食品'),
        (1,'饮料'),
        (2,'调料'),
        (3,'生活用品'),
        (4,'化妆品'),
        (5,'手机卡'),
        (6,'外卖'),
    ]
    GOODS_PREFERENTIAL = [
        (0,'无优惠'),
        (1, '特价优惠'),
        (2, '会员优惠'),
        (3, '优惠券优惠'),
    ]

    goods_name = models.CharField(max_length=32,verbose_name='商品名称',unique=True)
    goods_category = models.IntegerField(choices=CATEGORY_ITEM,verbose_name='商品类别')
    goods_image = models.ImageField(upload_to='goods/',verbose_name='商品图片')
    goods_introduction = models.CharField(max_length=64,verbose_name='商品介绍')
    goods_evaluation = models.CharField(max_length=128,verbose_name='商品评价')
    goods_sell_price = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='商品售价')
    goods_sell_volume = models.IntegerField(verbose_name='商品销量')
    goods_preferential = models.IntegerField(choices=GOODS_PREFERENTIAL,verbose_name='优惠方式',default=0)
    goods_preferential_price = models.DecimalField(max_digits=9,decimal_places=2,verbose_name='优惠价格',default=999)

# 商品库存模块
class goods_background(models.Model):

    STATE_ITEM=[
        (0,'缺货'),
        (1, '正常'),
        (2,'数量过多'),
    ]

    goods_id = models.OneToOneField(goods,on_delete=models.CASCADE,verbose_name='商品展示一对一关联')
    goods_number = models.CharField(max_length=13,verbose_name='商品条形码')
    goods_inventory = models.IntegerField(verbose_name='商品库存')
    goods_state = models.IntegerField(choices=STATE_ITEM,verbose_name='库存状态')
    goods_weight = models.FloatField(verbose_name='商品重量')
    goods_return = models.IntegerField(verbose_name='商品退货量')
    goods_exchange=models.IntegerField(verbose_name='商品换货量')
    goods_ereason = models.CharField(max_length=128,verbose_name='商品退换货理由')

# 商品采购模块
class goods_purchase(models.Model):
    goods_id = models.ForeignKey(goods,on_delete=models.CASCADE,verbose_name='商品展示外键关联')
    goods_background_id = models.ForeignKey(goods_background,on_delete=models.CASCADE,verbose_name='商品后台展示外键关联')
    goods_commodities_price = models.FloatField(verbose_name='商品采购价')
    goods_commodities_count = models.IntegerField(verbose_name='商品进货量')
    goods_commodities_freight = models.FloatField(verbose_name='商品采购运费')
    goods_purchase_date = models.DateField(verbose_name='商品进货日期')
    goods_production_date = models.DateField(verbose_name='商品生产日期')
    goods_shelf_date = models.IntegerField(verbose_name='商品保质期')









