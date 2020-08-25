from django.contrib import admin
from user.models import *
# Register your models here.

class user_admin(admin.ModelAdmin):

    list_display = ('id','user_name','user_password','user_gender',
                    'user_number','user_email','user_creat_time','user_state',)
    list_filter = ('user_gender','user_state')
    search_fields = ('user_name','user_number','user_email')
admin.site.register(user,user_admin)