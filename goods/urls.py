from django.urls import path
from . import views
# from cart import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product_list/', views.product_list, name='product_list'),
    path('goods_search/',views.goods_search,name='goods_search'),
]
