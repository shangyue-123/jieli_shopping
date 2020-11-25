from django.contrib import admin
from discounts.models import *
# Register your models here.

@admin.register(goods_special)
class goods_special_admin(admin.ModelAdmin):

    list_display = ('id','goods','preferential_price')
    search_fields = ('id','goods','preferential_price')

@admin.register(integral)
class integral_admin(admin.ModelAdmin):
    list_display = ('id','user','number')
    search_fields = ('id', 'user', 'number')
