import json

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from user.models import user
from .models import order
# Create your views here.

# 接收请求，在我的订单展示订单信息
def order_show(request):
    if request.method == 'GET':
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name=user_name).id
        order_dic_tuple = order.objects.filter(user_id=user_id).exclude(order_status=8)
        return render(request,'order.html',{'order_dic_tuple':order_dic_tuple})

def order_status_change(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order_status = request.POST.get('order_status')
        order.objects.filter(id=order_id).update(order_status=order_status)
        print('修改成功')
        return HttpResponse('修改成功')

# 查找待支付订单
def order_unpaid(request):
    if request.method == 'GET':
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name=user_name).id
        order_dic_tuple = order.objects.filter(Q(user_id=user_id) & Q(order_status=0))
        return render(request, 'order_unpaid.html', {'order_dic_tuple': order_dic_tuple})
# 查找待发货订单
def order_await(request):
    if request.method == 'GET':
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name=user_name).id
        order_dic_tuple = order.objects.filter(Q(user_id=user_id) & Q(order_status=1))
        return render(request, 'order_unpaid.html', {'order_dic_tuple': order_dic_tuple})

def order_receiving(request):
    if request.method == 'GET':
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name=user_name).id
        order_dic_tuple = order.objects.filter(Q(user_id=user_id) & Q(order_status=2))
        return render(request, 'order_unpaid.html', {'order_dic_tuple': order_dic_tuple})




