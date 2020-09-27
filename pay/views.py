import json

from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_POST

from cart.models import cart
from user.models import user, consignee
from order.models import order


# 接收购买请求，修改数据库商品数量，跳转支付界面
@require_POST
def pay(request):
    if request.method == 'POST':
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name = user_name).id
        consignee_dic = consignee.objects.filter(Q(consignee_default=1) & Q(user_id=user_id))
        goods_message = request.POST.get('goods_message')
        goods_message_dic = eval(goods_message)
        goods_message_list = list(goods_message_dic.values())
        print(goods_message_list)
        for goods_dic in goods_message_list:
            print(goods_dic)
            goods_id = goods_dic['goods_id']
            cart.objects.filter(Q(user_id=user_id) & Q(goods_id=goods_id)).update(
                cart_goods_quantity=0)
        return render(request,'pay.html',{'goods_message_list':goods_message_list,'consignee_dic':consignee_dic})

# 接收订单信息，将订单信息存入数据库
def submit_order(request):
    if request.method == 'POST':
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name=user_name).id
        goods_json = request.POST.get('goods_json')
        goods_json_dic = eval(goods_json)
        goods_json_list = list(goods_json_dic.values())
        payment_method = request.POST.get('payment_method')
        payment_amount = request.POST.get('payment_amount')[1:]
        consignee_id = request.POST.get('consignee_id')


        order.objects.create(order_status=0,payment_amount=payment_amount,
                             payment_method=payment_method,consignee_id=consignee_id,
                             user_id=user_id,goods_json=goods_json_list )
        return render(request,'index.html')






