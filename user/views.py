import json
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from django.views.decorators.http import require_POST

from user.models import *


# Create your views here.

def index(request):
    return render(request,'index.html')

# 提交注册信息，返回主页，储存session,发送cooky
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

        new_user = User.objects.create_user(username=user_name,password=user_password)
        print('新用户%s注册成功' % user_name)

        # 将session写入用户信息
        request.session['user_name'] = db.user_name
        request.session['user_id'] = db.id
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
@login_required
def login(request):
    # next = request.GET.get('next','')
    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        # 获取登录信息
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('user_password')
        # 验证登录成功后退回首页
        user_check = auth.authenticate(username=user_name,password=user_password)
        print(user_check)
        if user_check:
            auth.login(request,user_check)
            return  redirect('index.html')
            # if next == '':
            #     return  HttpResponseRedirect
            # else:
            #     return  render()
        else:
            err_msg = "账号密码不一致"
            return render(request,'login.html',{'script':"alert","wrong":err_msg})







