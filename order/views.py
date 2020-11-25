import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from user.models import user
from .models import order
from discounts.models import integral
import math
# Create your views here.

# 接收请求，在我的订单展示订单信息
def order_show(request):
    if request.method == 'GET':
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name=user_name).id
        # 获取检索的次数
        time_str = request.GET.get('time')
        #获取订单类别
        if time_str == None:
            time_str = 0
        time = int(time_str)
        start = time * 5
        stop = time * 5 + 5
        order_status = request.GET.get('order_status')
        if order_status == None:
            # 获取5个订单信息，在我的订单中显示
            order_dic = order.objects.filter(user_id=user_id).exclude(order_status=8)
            order_dic_tuple = order_dic.order_by('-id')[start:stop]
            order_dic_count = order_dic.count()
        else:
            # 获取5个订单信息，在我的订单中显示
            order_dic = order.objects.filter(Q(user_id=user_id) & Q(order_status = order_status)).exclude(order_status=8)
            order_dic_tuple = order_dic.order_by('-id')[start:stop]
            order_dic_count = order_dic.count()

        return render(request,'order.html',{'order_dic_tuple':order_dic_tuple,"order_dic_count":order_dic_count})

# 接收订单信息和订单管理修改请求，并回复修改成功
def order_status_change(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order_status = request.POST.get('order_status')
        if order_status == '3':
            user_obj = order.objects.get(id=order_id).user
            user_id = user_obj.id
            payment_amount = order.objects.get(id=order_id).payment_amount
            integral_number = order.objects.get(id=order_id).integral_number
            user_referrer = user.objects.get(id=user_id).user_referrer
            if integral_number == 0:
                # 获取用户积分
                invite_user_number = integral.objects.filter(user=user_obj).last().number
                if user_referrer != 'null':
                    referrer_obj = user.objects.get(id=user_referrer)
                    invite_referrer_number = integral.objects.filter(user=referrer_obj).last().number
                # 根据消费金额计算获取积分数量(每100元获得100积分),向上取整
                number_get = math.ceil(payment_amount)
                # 订单完成，为用户发放积分
                integral.objects.create(user=user_obj, change_reason=2, change=number_get, number=invite_user_number + number_get)
                #订单完成，为推荐用户发放积分
                integral.objects.create(user=referrer_obj,change_reason=2, change=number_get, number=invite_referrer_number + number_get)
            # else:
        order.objects.filter(id=order_id).update(order_status=order_status)
        # print('修改成功')
        return HttpResponse('修改成功')

