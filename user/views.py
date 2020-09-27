import json
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from  django.db.models import Q
from order.models import order
# from user.models import order


from user.models import *


# Create your views here.

def index(request):

    return render(request,'index.html')

# 提交注册信息，返回主页，储存session
def register(request):
    # 返回注册页面
    if request.method == 'GET':
        return render(request, 'register.html')

    # 接收注册数据存入数据库并返回首页
    elif request.method == 'POST':

        # 获取数据
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')
        user_gender = request.POST.get('user_gender')
        user_number = request.POST.get('user_number')
        user_email = request.POST.get('user_email')

        # 向user_user数据库传入数据
        db = user()
        db.user_name = user_name
        db.user_password = make_password(user_password,None,'pbkdf2_sha256')
        db.user_gender = user_gender
        db.user_number = user_number
        db.user_email = user_email
        db.save()

        User.objects.create_user(username=user_name,password=user_password)
        print('新用户%s注册成功' % user_name)

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
        return render(request,'index.html')


#接收注册页的AJAX用户名和邮箱验证
@require_POST
def register_check(request):
    # 获取网页提交来的数据
    user_name = request.POST.get('user_name')
    user_email = request.POST.get('user_email')
    #用户名是否存在
    name_msg = User.objects.filter(username=user_name).exists()
    email_msg = User.objects.filter(email = user_email).exists()
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
        print(user_name)
        user_password = request.POST.get('user_password')
        print(user_password)
        # 验证登录成功后退回首页
        user_check = auth.authenticate(username=user_name,password=user_password)
        print(user_check)
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
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name=user_name).id
        consignee_dic = consignee.objects.filter(Q(consignee_default=1) & Q(user_id=user_id))
        order_filter = order.objects.filter(user_id=user_id)
        order_count = order_filter.exclude(order_status=8).count()
        order_unpaid_count = order_filter.filter(order_status=0).count()
        order_await_count = order_filter.filter(order_status=1).count()
        order_receiving_count = order_filter.filter(order_status=2).count()
        print(consignee_dic)
        render_dic = {'consignee_dic':consignee_dic,'order_unpaid_count':order_unpaid_count,
                      'order_await_count':order_await_count,'order_receiving_count':order_receiving_count,
                      'order_count':order_count}
        return render(request,'personal_information.html',render_dic)

# 地址显示界面
def address(request):
    if request.method == 'GET':
        user_name = request.session.get('user_name')
        user_id = user.objects.get(user_name=user_name).id
        consignee_dic = consignee.objects.filter(user_id=user_id)
        print(consignee_dic)
        return render(request,'address.html',{'consignee_dic':consignee_dic})
    if request.method == 'POST':
        consignee_name = request.POST.get('consignee_name')
        consignee_number = request.POST.get('consignee_number')
        consignee_id = request.POST.get('consignee_id')
        consignee_address = request.POST.get('consignee_address')

        consignee_default = consignee.objects.get(id=consignee_id).consignee_default

        print(consignee_name, consignee_number, consignee_id, consignee_address, consignee_default)

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
        print(consignee_name,consignee_number,consignee_address,
              consignee_default,user_name,consignee_id,user_id)
        defaults = {'user_id':user_id,'consignee_name':consignee_name,
                    'consignee_number':consignee_number,'consignee_address':consignee_address,}
        if consignee_default == 'on':
            print('进入on')
            consignee_search = consignee.objects.filter(Q(consignee_default=1) & Q(user_id=user_id))
            print(consignee_search)
            consignee_check = consignee_search.exists()
            print(consignee_check)
            if consignee_check == True:
                if not consignee_id:
                    defaults['consignee_default']=1
                    consignee_search.update(consignee_default=0)
                    print('取消原来默认成功')
                    consignee.objects.update_or_create(defaults=defaults)
                    print('创建修改默认地址成功')
                else:
                    defaults['consignee_default'] = 1
                    consignee_search.update(consignee_default=0)
                    print('取消原来默认成功')
                    consignee.objects.update_or_create(defaults=defaults,id=consignee_id)
                    print('创建修改默认地址成功')


            else:
                consignee.objects.create(user_id=user_id,consignee_name=consignee_name,
                                         consignee_number=consignee_number,consignee_address=consignee_address,
                                         consignee_default=1)
        else:
            consignee.objects.create(user_id=user_id,consignee_name=consignee_name,
                                     consignee_number=consignee_number,consignee_address=consignee_address,
                                     consignee_default=0)
            print('创建地址成功')
        consignee_dic = consignee.objects.filter(user_id=user_id)
        return render(request, 'address.html',{'consignee_dic':consignee_dic})








