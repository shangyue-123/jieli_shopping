from django.shortcuts import render
from goods.models import *
# Create your views here.
# 接收物品类型，读取数据库相应物品信息，发送给前端
def product_list(request):
    if request.method == 'GET':
        goods_dic = goods.objects.all()
        print(goods_dic)
        return render(request,'product_list.html',{'goods_dic':goods_dic})
    elif request.method == 'POST':
        pass








