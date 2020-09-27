from django.contrib import admin
from user.models import *
# Register your models here.

@admin.register(user)
class user_admin(admin.ModelAdmin):

    list_display = ('id','user_name','user_password','user_gender',
                    'user_number','user_email','user_creat_time','user_state',)
    list_filter = ('user_gender','user_state')
    search_fields = ('user_name','user_number','user_email')

@admin.register(consignee)
class consignee_admin(admin.ModelAdmin):
    list_display =('user','consignee_name','consignee_number',
                   'consignee_address','consignee_default',)
    list_filter = ('user','consignee_default',)
    search_fields = ('user','consignee_name','consignee_number','consignee_address',)


# admin.site.register(user, user_admin)


