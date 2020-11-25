from django.contrib import admin
from order.models import order
# Register your models here.
@admin.register(order)
class order_admin(admin.ModelAdmin):
    list_display = ('user','order_status','order_time','goods_json')
    list_filter = ('user','order_status',)
    search_fields = ('user','order_status','order_time',)