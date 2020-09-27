from django.urls import path

from . import views

urlpatterns = [
    path('',views.pay,name='pay'),
    path('pay/',views.pay,name= 'pay'),
    path('submit_order/',views.submit_order,name='submit_order'),
    # path('order_success/',views.order_success,name='order_success')
]
