from django.urls import path

from . import views

urlpatterns = [
    path('',views.pay,name='pay'),
    path('pay/',views.pay,name= 'pay'),
    path('submit_order/',views.submit_order,name='submit_order'),
    path('pay_address_change/',views.pay_address_change,name='pay_address_change'),
    path('goods_sell_volume_add/',views.goods_sell_volume_add,name='goods_sell_volume_add'),
    # path('order_success/',views.order_success,name='order_success')
]
