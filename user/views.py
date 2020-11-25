import json
import random
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.core.mail import send_mail
from jieli_shopping.settings import EMAIL_FROM
from order.models import order
from discounts.models import *
from discounts.views import use_recommend_QR
# from user.models import invite
from discounts.models import goods_special
from goods.models import goods
# from user.models import order
from user.models import *


# Create your views here.
# 显示首页，传输限时特价信息
def index(request):
    if request.method == 'GET':
        goods_dic = goods.objects.filter(goods_special__goods_preferential=1)
        # print(goods_dic)
        # goods_dic = goods.objects.filter(goods_preferential=1)
    return render(request,'index.html',{'goods_dic':goods_dic})

# 提交注册信息，返回主页，储存session
def register(request):
    # 返回注册页面
    if request.method == 'GET':
        return render(request, 'register.html')

    # 接收注册数据存入数据库并返回首页
    elif request.method == 'POST':

        # 获取数据
        user_name = request.POST.get('user_name')
        user_password = make_password(request.POST.get('user_password'),None,'pbkdf2_sha256')
        user_gender = request.POST.get('user_gender')
        user_number = request.POST.get('user_number')
        user_email = request.POST.get('user_email')

        # 获取邀请码
        recommend_code = request.GET.get('recommend_code')

        # 向user_user数据库传入数据
        if not recommend_code is None:
            invite_user = invite.objects.get(code=recommend_code).user
            invite_user_id = invite_user.id
            db = user.objects.create(user_name=user_name,user_password=user_password,
                                     user_gender=user_gender,user_number=user_number,
                                     user_email=user_email,user_referrer=invite_user_id)
            # 获取推荐人积分
            invite_user_number = integral.objects.filter(user=invite_user).last().number
            # 注册完成为推荐人分发积分
            integral.objects.create(user=invite_user,change_reason=0,change=500,number=invite_user_number+500)
        else:
            db = user.objects.create(user_name=user_name, user_password=user_password,
                                     user_gender=user_gender, user_number=user_number,
                                     user_email=user_email,)

        # 想Django自带用户表传入信息
        User.objects.create_user(username=user_name,password=user_password,email=user_email)
        # print('新用户%s注册成功' % user_name)

        # 注册完成赠送100积分
        integral.objects.create(user=db,change_reason=4,change=100,number=100)



        # 为用户添加分享获积分二维码
        user_id = user.objects.get(user_name=user_name).id
        use_recommend_QR(user_id=user_id)

        # 核对用户名密码
        user_check = auth.authenticate(username=user_name, password=user_password)
        auth.login(request, user_check)
        request.session['user_name'] = user_name
        request.session['is_login'] = True

        # 将用户信息写入session
        # auth.login(request, user_name)
        # request.session['user_name'] = user_name
        # request.session['is_login'] = True


        # auth.login(request, user_check)
        # 返回注册成功并跳转页面
        return HttpResponseRedirect('/index/')


#接收注册页的AJAX用户名和邮箱验证
@require_POST
def register_check(request):
    # 获取网页提交来的数据
    user_name = request.POST.get('user_name')
    user_email = request.POST.get('user_email')
    #用户名是否存在
    name_msg = user.objects.filter(user_name=user_name).exists()
    email_msg = user.objects.filter(user_email = user_email).exists()
    msg = {'name_msg':name_msg,'email_msg':email_msg}
    # 转换为JSON格式发送
    return HttpResponse(json.dumps(msg))

# 验证登录并跳转上一页
# @login_required
def login(request):
    # next = request.GET.get('next','')
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        # 获取登录信息
        user_name = request.POST.get('user_name')
        # print(user_name)
        user_password = request.POST.get('user_password')
        # print(user_password)
        # 验证登录成功后退回首页
        user_check = auth.authenticate(username=user_name,password=user_password)
        # print(user_check)
        if user_check:
            auth.login(request,user_check)
            request.session['user_name'] = user_name
            request.session['is_login'] = True
            return  redirect('index')
            # if next == '':
            #     return  HttpResponseRedirect
            # else:
            #     return  render()
        else:
            err_msg = "账号密码不一致"
            return render(request,'login.html',{'script':"alert","wrong":err_msg})


# 退出登录
def logout(request):
    if request.method == "GET":
        request.session.clear()
        return redirect("/index/")

@login_required
# 个人信息界面
def personal_information(request):
    if request.method == 'GET':
        # 获取用户id
        user_name = request.session.get('user_name')
        user_get = user.objects.get(user_name=user_name)
        user_id = user_get.id
        # 获取用户地址信息
        consignee_dic = consignee.objects.filter(Q(consignee_default=1) & Q(user_id=user_id))
        # 获取用户订单信息
        order_filter = order.objects.filter(user_id=user_id)
        order_count = order_filter.exclude(order_status=8).count()
        order_unpaid_count = order_filter.filter(order_status=0).count()
        order_await_count = order_filter.filter(order_status=1).count()
        order_receiving_count = order_filter.filter(order_status=2).count()
        # 获取用户积分信息
        # 检测积分是否存在，存在则获取最新的积分信息中的积分数量，不存在则创建积分数据
        integral_number_boole = integral.objects.filter(user=user_id).exists()
        if integral_number_boole:
            integral_number = integral.objects.filter(user=user_id).last().number
        else:
            integral.objects.create(user=user_get,change_reason=4,change=100,number=100)
            integral_number = 100
        #获取推荐二维码路径信息
        qr_boole = invite.objects.filter(user=user_id).exists()
        if qr_boole :
            qr = invite.objects.get(user=user_id).qr
        else:
            use_recommend_QR(user_id)
            qr = invite.objects.get(user=user_id).qr
        render_dic = {'consignee_dic':consignee_dic,'order_unpaid_count':order_unpaid_count,
                      'order_await_count':order_await_count,'order_receiving_count':order_receiving_count,
                      'order_count':order_count,'integral_number':integral_number,'qr':qr}
        return render(request,'personal_information.html',render_dic)

# 地址显示界面
def address(request):
    if request.method == 'GET':
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name=user_name).id
        consignee_dic = consignee.objects.filter(user_id=user_id)
        order_id = request.GET.get('order_id')
        # print(order_id)
        # print(consignee_dic)
        return render(request,'address.html',{'consignee_dic':consignee_dic,'order_id':order_id})
    if request.method == 'POST':
        consignee_name = request.POST.get('consignee_name')
        consignee_number = request.POST.get('consignee_number')
        consignee_id = request.POST.get('consignee_id')
        consignee_address = request.POST.get('consignee_address')

        consignee_default = consignee.objects.get(id=consignee_id).consignee_default

        # print(consignee_name, consignee_number, consignee_id, consignee_address, consignee_default)

        consignee_dic = {'consignee_name': consignee_name, 'consignee_number': consignee_number,
                         'consignee_id': consignee_id, 'consignee_address': consignee_address,
                         "consignee_default": consignee_default}

        return render(request, 'address_change.html', consignee_dic)

# 地址变更界面
def address_change(request):
    if request.method == 'GET':
        return render(request,'address_change.html')
    if request.method == 'POST':
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name=user_name).id
        consignee_id = request.POST.get('consignee_id')
        consignee_name = request.POST.get('consignee_name')
        consignee_number = request.POST.get('consignee_number')
        consignee_address = request.POST.get('consignee_address')
        consignee_default = request.POST.get('consignee_default')
        order_id = request.GET.get('order_id')
        print(consignee_name,consignee_number,consignee_address,
              consignee_default,user_name,consignee_id,user_id)
        defaults = {'user_id':user_id,'consignee_name':consignee_name,
                    'consignee_number':consignee_number,'consignee_address':consignee_address,}
        # 如果设置为默认则：
        if consignee_default == 'on':
            # print('进入on')
            # 搜索该用户是否有默认地址
            consignee_search = consignee.objects.filter(Q(consignee_default=1) & Q(user_id=user_id))
            # print(consignee_search)
            # 如果有默认地址，返回True;没有，返回False
            consignee_check = consignee_search.exists()
            # print(consignee_check)
            if consignee_check == True:
                # 如果有默认地址，并且是不存在的地址信息
                if not consignee_id:
                    defaults['consignee_default'] = 1
                    # 取消原来默认
                    consignee_search.update(consignee_default=0)
                    # print('取消原来默认成功')
                    # 修改默认地址
                    consignee.objects.create(**defaults)
                    # print('创建修改默认地址成功')
                #   有默认地址，修改已有地址信息
                else:
                    consignee_search.update(consignee_default=0)
                    # print('取消原来默认成功')
                    consignee.objects.filter(id=consignee_id).update(consignee_default=1,**defaults)
                    # print('创建修改默认地址成功')

            # 如果没有该用户的默认地址，则新创建
            else:
                consignee.objects.create(consignee_default=1,**defaults)
        # 如果该用户未设置默认
        else:
            consignee.objects.create(consignee_default=0,**defaults)
            print('创建地址成功')
        consignee_dic = consignee.objects.filter(user_id=user_id)
        return render(request, 'address.html',{'consignee_dic':consignee_dic,'order_id':order_id})

# 找回账号密码
def retrieve(request):
    if request.method == 'GET':
        return render(request,'retrieve.html')
    if request.method == 'POST':
        user_email = request.POST.get("user_email")
        verification = request.POST.get("verification")
        verification_check = request.session.get("verification")
        retrieve_kind = request.POST.get('retrieve_kind')
        user_name = user.objects.get(user_email=user_email).user_name
        if verification.lower() == verification_check.lower():
            if retrieve_kind == 'name':
                return render(request,"retrieve_name.html",{'user_name':user_name})
            elif retrieve_kind == 'password':
                return render(request, "retrieve_password.html",{'user_email':user_email,'user_name':user_name})
        else:
            return HttpResponseRedirect('/index/')

# get请求获取验证码，post请求验证验证码是否正确
def email_verification(request):
    # 发送验证码
    if request.method == 'GET':
        user_email = request.GET.get('user_email')
        verification = random_verification()
        # 将验证码信息存入session
        request.session["verification"] = verification
        # 设置验证码有效时间
        request.session.set_expiry(300)
        # 邮箱发送
        email_title = 'jieli_shopping验证码'
        email_body = '验证码为:{}'.format(verification)
        send_mail(email_title,email_body,EMAIL_FROM,[user_email,])

        return HttpResponse('True')
    # 验证验证码信息
    if request.method == 'POST':
        email_verification = request.POST.get('email_verification')
        verification = request.session.get('verification')
        if email_verification.lower() == verification.lower():
            return HttpResponse('true')
        else:
            return HttpResponse('false')

#     修改密码，找回密码
def password_change(request):
    if request.method == 'POST':
        password_new = request.POST.get("password_new")
        password = make_password(password_new,None,'pbkdf2_sha256')
        user_email = request.POST.get("user_email")
        user_name = request.POST.get("user_name")
        user.objects.filter(user_name=user_name).update(user_password=password)
        User.objects.filter(username=user_name).update(password=password)
        print(password_new,user_email,password,user_name)
        return HttpResponseRedirect('/user/login/')

# 生成验证码
def random_verification(randomlength=4):
    verification_parameter = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    # 生成验证码数组
    verification_arr = random.sample(verification_parameter,randomlength)
    # 将验证码拼合
    verification = ''.join(verification_arr)
    print(verification)
    return verification











