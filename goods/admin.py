from django.contrib import admin
from goods.models import *

class goods_admin(admin.ModelAdmin):
    list_display = ('goods_name','goods_category','goods_image','goods_introduction',
                    'goods_evaluation','goods_sell_price','goods_sell_volume',
                    'goods_preferential','goods_preferential_price')
    list_filter = ('goods_preferential','goods_category')
    search_fields = ('goods_name','goods_category','goods_image','goods_introduction',
                    'goods_evaluation','goods_sell_price','goods_sell_volume')

class goods_background_admin(admin.ModelAdmin):
    list_display = ('goods_id','goods_number','goods_inventory','goods_state',
                    'goods_weight','goods_return','goods_exchange','goods_ereason')
    list_filter = ('goods_state',)
    search_fields = ('goods_id','goods_number')

class goods_purchase_admin(admin.ModelAdmin):
    list_display = ('goods_background_id','goods_commodities_price',
                    'goods_commodities_count','goods_commodities_freight',
                    'goods_purchase_date','goods_production_date','goods_shelf_date',)
    list_filter = ('goods_production_date',)
    search_fields = ('goods_production_date','goods_shelf_date',)
# Register your models here.
admin.site.register(goods,goods_admin)
admin.site.register(goods_background,goods_background_admin)
admin.site.register(goods_purchase,goods_purchase_admin)
