import json

from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_POST

from cart.models import cart
from user.models import user, consignee
from order.models import order
from goods.models import goods
from discounts.models import *



# 接收购买请求，修改数据库商品数量，跳转支付界面
@require_POST
def pay(request):
    # 待完成，接收address_change的get请求，根据传入的order_id搜索订单，并重新显示订单
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        # 获取前端信息
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name = user_name).id
        integral_number = integral.objects.filter(user=user_id).last().number
        consignee_dic = consignee.objects.filter(Q(consignee_default=1) & Q(user_id=user_id)).first()
        payment_amount = request.POST.get('payment_amount')
        goods_message = request.POST.get('goods_message')
        goods_message_dic = eval(goods_message)
        goods_message_list = list(goods_message_dic.values())
        # 购物车点击结算，不在购物车显示该商品信息
        for goods_dic in goods_message_list:
            # print(goods_dic)
            goods_id = goods_dic['goods_id']
            cart.objects.filter(Q(user_id=user_id) & Q(goods_id=goods_id)).update(
                cart_goods_quantity=0)
        #   如果无收件人信息，则不存收件人信息
        if consignee_dic == None:
            order_insert = order.objects.create(user_name=user_name, payment_amount=payment_amount, payment_method=0,
                                                goods_json=goods_message_list,order_status=0,user_id=user_id,)
            order_id = order_insert.id
            pay_dic = {'goods_message_list':goods_message_list,'order_id':order_id,'integral_number':integral_number}
        #     有收件人信息，保存收件人信息
        else:
            consignee_name = consignee_dic.consignee_name
            consignee_number = consignee_dic.consignee_number
            consignee_address = consignee_dic.consignee_address

            order_insert = order.objects.create(user_name=user_name,payment_amount=payment_amount, payment_method=0,
                                 consignee_name=consignee_name,consignee_number=consignee_number,goods_json=goods_message_list,
                                 consignee_address=consignee_address,order_status=0,
                                 user_id=user_id,)
            order_id = order_insert.id
            pay_dic = {'goods_message_list':goods_message_list,'consignee_name':consignee_name,
                       'consignee_number':consignee_number,'consignee_address':consignee_address,
                       'order_id':order_id,'integral_number':integral_number}
        return render(request,'pay.html',pay_dic)

# 接收订单信息，将订单信息存入数据库
def submit_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        user_name = request.session.get('user_name')
        user_user = user.objects.get(user_name=user_name)
        user_id =user_user.id
        goods_json = request.POST.get('goods_json')
        goods_json_dic = eval(goods_json)
        goods_json_list = list(goods_json_dic.values())
        payment_amount = request.POST.get('payment_amount')[1:]
        payment_method = request.POST.get('payment_method')
        consignee_name = request.POST.get('consignee_name')
        consignee_number = request.POST.get('consignee_number')
        consignee_address = request.POST.get('consignee_address')
        integral_number = int(request.POST.get('integral_number'))
        #  如果现金支付方式，跳过待付款环节
        if payment_method == '0':
            order_find = order.objects.filter(id=order_id)
            order_find.update(user_name=user_name,goods_json=goods_json_list,
                              payment_amount=payment_amount,payment_method=payment_method,consignee_name=consignee_name,
                              consignee_number=consignee_number,consignee_address=consignee_address,
                              order_status=1,user_id=user_id,integral_number=integral_number,)
        # 如果为微信支付或者支付宝支付，则订单状态为待支付
        else:
            order_find = order.objects.filter(id=order_id)
            order_find.update(user_name=user_name,goods_json=goods_json_list,
                              payment_amount=payment_amount,payment_method=payment_method,consignee_name=consignee_name,
                              consignee_number=consignee_number,consignee_address=consignee_address,
                              order_status=0,user_id=user_id,integral_number=integral_number,)
        # 数据库记录使用积分
        if integral_number != 0:
            number = integral.objects.filter(user=user_id).last().number
            integral.objects.create(user=user_user,change_reason=6,change=-integral_number,number=number-integral_number)

        return HttpResponseRedirect('/index/')


# 接收支付页面地址修改请求
def pay_address_change(request):

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        consignee_name = request.POST.get('consignee_name')
        consignee_number = request.POST.get('consignee_number')
        consignee_address = request.POST.get('consignee_address')
        print(consignee_name,consignee_number,consignee_address,order_id)
        order.objects.filter(id=order_id).update(consignee_name=consignee_name,
                                                 consignee_number=consignee_number,
                                                 consignee_address=consignee_address)
        goods_message_list = order.objects.get(id=order_id).goods_json

        pay_dic = {'goods_message_list': goods_message_list, 'consignee_name': consignee_name,
                   'consignee_number': consignee_number, 'consignee_address': consignee_address,
                   'order_id': order_id}
        return render(request,'pay.html',pay_dic)

# 提交订单时更改商品销量数量
def goods_sell_volume_add(request):
    if request.method == 'POST':
        goods_id_json = request.POST.get("goods_id_json")
        goods_id_dic = json.loads(goods_id_json)
        # 遍历所有商品id，为商品添加销量
        for goods_id in goods_id_dic.keys():
            goods_sell_volume = goods.objects.get(id=goods_id).goods_sell_volume
            goods_sell_volume_add = int(goods_id_dic[goods_id])
            goods.objects.filter(id=goods_id).update(goods_sell_volume=goods_sell_volume+goods_sell_volume_add)
        return HttpResponse('success')





