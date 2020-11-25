import json
from itertools import chain

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from user.models import user
from cart.models import cart
from goods.models import goods
from django.db.models import Q, Sum
from django.contrib.auth.decorators import login_required
from discounts.models import goods_special


# Create your views here.
# 显示购物车商品信息
@login_required
def cart_list(request):
    if request.method == 'GET':
        search_list = []
        # 获取检索的次数
        time_str = request.GET.get('time')
        if time_str == None:
            time_str = 0
        time = int(time_str)
        start = time * 15
        stop = time * 15 + 15
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name=user_name).id
        cart_dic = cart.objects.filter(Q(user_id=user_id) & ~Q(cart_goods_quantity=0)).order_by('-id')[start:stop]
        print(cart_dic)
        goods_count = cart.objects.filter(Q(user_id=user_id) & ~Q(cart_goods_quantity=0)).count()
        print(goods_count)
        # 遍历购物车数据库，提取需要的数据
        for c in cart_dic:
            goods_id = c.goods_id
            cart_goods_quantity = c.cart_goods_quantity
            goods_name = goods.objects.get(id=goods_id).goods_name
            goods_sell_price = goods.objects.get(id=goods_id).goods_sell_price
            goods_image = goods.objects.get(id=goods_id).goods_image
            if cart_goods_quantity == 0:
                continue
            else:
                search_list.append({'goods_name': goods_name, 'goods_sell_price': goods_sell_price,
                                    'cart_goods_quantity': cart_goods_quantity,'goods_id':goods_id,
                                    'goods_image':goods_image,})
        return render(request, 'cart_list.html', {'search_list': search_list,'goods_count':goods_count})

    # 接收购物车信息页AJAX请求，显示特价
    elif request.method == 'POST':
        goods_preferential_dic_list = goods_special.objects.filter(goods_preferential=1).values('goods','preferential_price','goods_preferential')
        data = list(goods_preferential_dic_list)
        return JsonResponse(data,safe=False)

# 加入购物车时，传入数据库，并改变前端购物车徽章的数字
@require_POST
def cart_change(request):
    # 接收前端传来的数据
    goods_id = request.POST.get('goods_id')
    cart_number = request.POST.get('cart_number')
    cart_type = request.POST.get('cart_type')
    user_name = request.session.get('user_name')
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
    cart_goods_quantity_sum_dic = cart.objects.filter(Q(user=user_id) & ~Q(cart_goods_quantity=0)).aggregate(Sum('cart_goods_quantity'))
    # 返回到购物车中对应商品数目
    cart_goods_quantity_sum_dic['cart_goods_quantity']=cart.objects.get(Q(user_id=user_id) & Q(goods_id=goods_id)).cart_goods_quantity
    # 传入前端数据{'cart_goods_quantity__sum': '购物车sum值', 'cart_goods_quantity': '对应商品数量'}
    return HttpResponse(json.dumps(cart_goods_quantity_sum_dic))


# 页面加载时显示购物车数量
@require_POST
def cart_number(request):

    user_name = request.session.get('user_name')
    if user_name is None:
        cart_goods_quantity_sum_dic = 0
    else:
        user_id = user.objects.get(user_name=user_name).id
        cart_goods_quantity_sum_dic = cart.objects.filter(user=user_id).aggregate(Sum('cart_goods_quantity'))
    return HttpResponse(json.dumps(cart_goods_quantity_sum_dic))






