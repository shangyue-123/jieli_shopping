from django.shortcuts import render

# Create your views here.
# 接收物品类型，读取数据库相应物品信息，发送给前端
def product_list(request):
    if request.method == 'GET':
        return render(request,'product_list.html')

    elif request.method == 'POST':
        pass