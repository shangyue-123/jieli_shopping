from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.cart_list, name='cart_list'),
    path('cart_list/', views.cart_list, name='cart_list'),
    path('cart_change/',views.cart_change,name='cart_change'),
    path('cart_number/',views.cart_number,name='cart_number'),
    # path('cart_search/<search_input>/',views.cart_search,name='cart_search'),
    # path('cart_search/',views.cart_search,name='cart_search'),
    # path('cart_search_input_skip/',views.cart_search_input_skip,name='cart_search_skip'),


]
