"""jieli_shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    #进入用户路由和首页
    path('',include('user.urls')),
    path('index/',include('user.urls')),
    path('user/',include('user.urls')),
    #进入商品路由
    path('goods/',include('goods.urls')),
    #进入购物车路由
    path('cart/',include('cart.urls')),
    #进入支付路由
    path('pay/',include('pay.urls')),
    path('order/',include('order.urls')),
    #进入后台管理路由
    path('order_manage/',include('order_manage.urls')),
    #进入优惠路由
    path('discounts/',include('discounts.urls'))


]
