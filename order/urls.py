from django.urls import path

from . import views

urlpatterns = [
    path('',views.order_show,name='order_show'),
    path('order_show/',views.order_show,name='order_show'),
    path('order_status_change/',views.order_status_change,name='order_status_change'),
    path('order_unpaid/',views.order_unpaid,name='order_unpaid'),
    path('order_await/',views.order_await,name='order_await'),
    path('order_receiving/',views.order_receiving,name='order_receiving')

]