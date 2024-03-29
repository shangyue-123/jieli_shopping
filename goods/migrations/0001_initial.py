# Generated by Django 3.1 on 2020-10-07 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=32, unique=True, verbose_name='商品名称')),
                ('goods_category', models.IntegerField(choices=[(0, '休闲零食'), (1, '火锅速食'), (2, '厨房调料'), (3, '生活用品'), (4, '厨房用品'), (5, '卫浴用品')], verbose_name='商品类别')),
                ('goods_image', models.ImageField(upload_to='goods/', verbose_name='商品图片')),
                ('goods_introduction', models.CharField(max_length=64, verbose_name='商品介绍')),
                ('goods_evaluation', models.CharField(max_length=128, verbose_name='商品评价')),
                ('goods_sell_price', models.FloatField(verbose_name='商品售价')),
                ('goods_sell_volume', models.IntegerField(verbose_name='商品销量')),
            ],
        ),
        migrations.CreateModel(
            name='goods_background',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_number', models.CharField(max_length=13, verbose_name='商品条形码')),
                ('goods_inventory', models.IntegerField(verbose_name='商品库存')),
                ('goods_state', models.IntegerField(choices=[(0, '缺货'), (1, '正常'), (2, '数量过多')], verbose_name='库存状态')),
                ('goods_weight', models.FloatField(verbose_name='商品重量')),
                ('goods_return', models.IntegerField(verbose_name='商品退货量')),
                ('goods_exchange', models.IntegerField(verbose_name='商品换货量')),
                ('goods_ereason', models.CharField(max_length=128, verbose_name='商品退换货理由')),
                ('goods_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='goods.goods', verbose_name='商品展示一对一关联')),
            ],
        ),
        migrations.CreateModel(
            name='goods_purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_commodities_price', models.FloatField(verbose_name='商品采购价')),
                ('goods_commodities_count', models.IntegerField(verbose_name='商品进货量')),
                ('goods_commodities_freight', models.FloatField(verbose_name='商品采购运费')),
                ('goods_purchase_date', models.DateField(verbose_name='商品进货日期')),
                ('goods_production_date', models.DateField(verbose_name='商品生产日期')),
                ('goods_shelf_date', models.IntegerField(verbose_name='商品保质期')),
                ('goods_background_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goods_background', verbose_name='商品后台展示外键关联')),
                ('goods_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goods', verbose_name='商品展示外键关联')),
            ],
        ),
    ]
