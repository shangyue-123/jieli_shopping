import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from user.models import *
from order.models import order
from django.core import serializers
from django.utils.timezone import localtime
from datetime import datetime
# Create your views here.

# 后台订单管理
def order_manage(request):
    if request.method == 'GET':
        user_name = request.session.get('user_name')
        user_list= user.objects.get(user_name=user_name)
        user_id = user_list.id
        user_super = user_list.user_super
        # print(user_name,user_id,user_super)
        if user_super == 0:
            return render(request,'index.html')
        if user_super == 1:
            order_dic_tuple = order.objects.all().exclude(order_status=8).order_by("-id")
            order_id_max = order_dic_tuple.first().id
            return render(request,'order_manage.html',{'order_dic_tuple':order_dic_tuple,'order_id_max':order_id_max})

# 显示新订单
def order_new(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        print("order_id:%s"%order_id)
        new_order_is = order.objects.filter(id__gt=order_id).exists()
        print(new_order_is)
        if new_order_is == False:
            print('没有新订单')
            return HttpResponse('None')
        else:
            new_order = order.objects.filter(id__gt=order_id)
            # for i in new_order:
            #     order_time = i.order_time
            #     order_time_change = localtime(order_time)
            #     print(type(order_time))
            #     print(type(order_time_change))
            #     i['order_time'] = order_time_change
            new_order_json = serializers.serialize("json",new_order)
            # print(new_order_json)
            return JsonResponse(new_order_json,safe=False)









