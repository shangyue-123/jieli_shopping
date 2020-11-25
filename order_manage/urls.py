from django.urls import path
from . import views

urlpatterns = [
    path('',views.order_manage,name='order_manage'),
    path('order_manage/',views.order_manage,name='order_manage'),
    path('order_new/',views.order_new,name='order_name'),
]