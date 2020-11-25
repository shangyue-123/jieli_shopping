from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from goods.models import *
from discounts.models import goods_special
import random
from django.core import serializers
import json
# Create your views here.
# get请求，搜索所有商品，发送给前端
# post请求，传输特价商品特价
def product_list(request):
    if request.method == 'GET':
        # 获取检索的次数
        time_str = request.GET.get('time')
        # 获取检索商品类别
        goods_category = request.GET.get('goods_category')

        if goods_category == None:
            goods_category = 0
        if time_str == None:
            time_str = 0
        time = int(time_str)
        start = time*10
        stop = time*10+10
        # 获取10个商品信息，在商品页面显示
        goods_dic = goods.objects.filter(goods_category=goods_category).order_by('id')[start:stop]
        goods_count = goods.objects.filter(goods_category=goods_category).count()
        return render(request,'product_list.html',{'goods_dic':goods_dic,'goods_count':goods_count,'goods_category':goods_category})
    elif request.method == 'POST':
        # 获取特价商品信息，在首页显示
        goods_preferential_dic_list = goods_special.objects.filter(goods_preferential=1).values('goods','preferential_price')
        data = list(goods_preferential_dic_list)
        return JsonResponse(data,safe=False)

#实时搜索商品，跳转商品页面
def goods_search(request):
    # 接收搜索商品请求内容，跳转到商品界面
    if request.method == 'GET':
        search_input = request.GET.get('search_input')
        goods_dic = goods.objects.filter(goods_name__icontains=search_input)
        return render(request,'product_list.html',{'search_input':search_input,'goods_dic':goods_dic})
    # 实时显示搜索提示框
    elif request.method == 'POST':
        goods_name_list = list()
        search_input = request.POST.get('search_input')
        try:
            search_goods = goods.objects.filter(goods_name__icontains=search_input)
            for s in search_goods:
                goods_name_list.append(s.goods_name)
        except ValueError:
            pass
        except UnboundLocalError:
            pass
        return JsonResponse(goods_name_list,safe=False)


















