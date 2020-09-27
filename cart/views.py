import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from user.models import user
from cart.models import cart
from goods.models import goods
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required


# Create your views here.
# 显示购物车商品信息
@login_required
def cart_list(request):
    if request.method == 'GET':
        search_list = []

        user_name = request.session.get('user_name')

        user_id = user.objects.get(user_name=user_name).id

        # print(user_id)
        cart_dic = cart.objects.filter(user_id=user_id)
        # print(cart_dic)

        for c in cart_dic:
            goods_name = goods.objects.get(id=c.goods_id).goods_name
            goods_sell_price = goods.objects.get(id=c.goods_id).goods_sell_price
            goods_image = goods.objects.get(id=c.goods_id).goods_image
            cart_goods_quantity = c.cart_goods_quantity
            if cart_goods_quantity == 0:
                continue
            else:
                search_list.append({'goods_name': goods_name, 'goods_sell_price': goods_sell_price,
                                    'cart_goods_quantity': cart_goods_quantity,'goods_id':c.goods_id,
                                    'goods_image':goods_image})
        # print(search_list)
        return render(request, 'cart_list.html', {'search_list': search_list})
    # 接收搜索请求，在购物车显示搜索信息
    elif request.method == 'POST':
        pass


# 购物车数据改变时，传入数据库，并改变前端购物车徽章的数字
@require_POST
def cart_change(request):
    # 接收前段传来的数据
    goods_id = request.POST.get('goods_id')
    # print(goods_id)
    cart_number = request.POST.get('cart_number')
    # print(cart_number)
    cart_type = request.POST.get('cart_type')
    # print(cart_type)
    user_name = request.session.get('user_name')
    # 从数据库搜索数据
    user_id = user.objects.get(user_name=user_name).id
    # 如果购物车信息存在，返回True,如果不存在，返回False
    cart_check = cart.objects.filter(Q(user_id=user_id) & Q(goods_id=goods_id)).exists()

    # 如果不存在，插入数据
    if cart_check == False:
        cart.objects.create(user_id=user_id, goods_id=goods_id, cart_goods_quantity=cart_number)
    # 如果存在，判断加减类型
    elif cart_check == True:
        # 如果是加，购物车商品数量+1
        if cart_type == "add":
            cart_target = cart.objects.get(Q(user_id=user_id) & Q(goods_id=goods_id))
            cart_goods_quantity = cart_target.cart_goods_quantity
            cart.objects.filter(Q(user_id=user_id) & Q(goods_id=goods_id)).update(
                cart_goods_quantity=1 + cart_goods_quantity)
        # 如果是减，购物车商品数量-1
        elif cart_type == "subtract":
            cart_target = cart.objects.get(Q(user_id=user_id) & Q(goods_id=goods_id))
            cart_goods_quantity = cart_target.cart_goods_quantity
            cart.objects.filter(Q(user_id=user_id) & Q(goods_id=goods_id)).update(
                cart_goods_quantity=cart_goods_quantity - 1)
    # 计算商品数量总数
    cart_goods_quantity_sum_dic = cart.objects.filter(user=user_id).aggregate(Sum('cart_goods_quantity'))
    # 返回到购物车中对应商品数目
    cart_goods_quantity_sum_dic['cart_goods_quantity']=cart.objects.get(Q(user_id=user_id) & Q(goods_id=goods_id)).cart_goods_quantity
    # 传入前端数据{'cart_goods_quantity__sum': '购物车sum值', 'cart_goods_quantity': '对应商品数量'}
    return HttpResponse(json.dumps(cart_goods_quantity_sum_dic))


# 页面加载时显示购物车数量
@require_POST
def cart_number(request):
    user_name = request.session.get('user_name')
    print(user_name)
    user_id = user.objects.get(user_name=user_name).id
    cart_goods_quantity_sum_dic = cart.objects.filter(user=user_id).aggregate(Sum('cart_goods_quantity'))
    print(cart_goods_quantity_sum_dic)
    return HttpResponse(json.dumps(cart_goods_quantity_sum_dic))

#实时搜索商品，跳转商品页面
def cart_search(request):
    # 接收搜索商品请求内容，跳转到商品界面
    if request.method == 'GET':
        search_input = request.GET.get('search_input')
        print(search_input)
        goods_dic = goods.objects.filter(goods_name__icontains=search_input)
        return render(request,'product_list.html',{'goods_dic':goods_dic})
    # 实时显示搜索提示框
    elif request.method == 'POST':
        goods_name_list = list()
        search_input = request.POST.get('search_input')
        search_goods = goods.objects.filter(goods_name__icontains=search_input)
        print(search_goods)
        for s in search_goods:
            goods_name_list.append(s.goods_name)
        print(goods_name_list)
        return JsonResponse(goods_name_list,safe=False)





