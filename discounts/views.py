from django.shortcuts import render
from goods.models import goods
from user.models import user,invite
from discounts.models import integral
from discounts.models import goods_special
# Create your views here.
import random
import qrcode
import string


def use_recommend_QR(user_id):
    user_id_str = str(user_id)
    user_id_len = len(user_id_str)
    recommend_code = user_id_str
    for i in range(0,8-user_id_len):
        recommend_code += random.choice(string.digits)

    qr = qrcode.QRCode(version=5,box_size=8,border=4)
    qr.add_data('http://106.54.70.248:8000/user/register/?recommend_code={}'.format(recommend_code))
    qr.make(fit=True)
    img = qr.make_image()
    user_model = user.objects.get(id=user_id)
    user_creat_time = user_model.user_creat_time
    user_creat_time = str(user_creat_time).replace('-','')
    filename = user_id_str+user_creat_time+recommend_code
    file_load ='user_QR/{}.png'.format(filename)
    img.save('static/media/'+file_load)

    invite.objects.create(user=user_model,code=recommend_code,qr=file_load)



#每晚0点（韩国时间），更新限时特惠商品
def goods_preferential_price_update():
    goods_special.objects.filter(goods_preferential=1).update(goods_preferential=0)
    goods_special_id_list = list(goods_special.objects.filter(goods_preferential=0).values_list('id', flat=True))
    goods_special_id_random = random.sample(goods_special_id_list,3)
    for goods_special_id in goods_special_id_random:
        goods_special.objects.filter(id=goods_special_id).update(goods_preferential=1)
    return '更新限时特惠成功'