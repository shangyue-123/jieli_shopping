from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='regster'),
    path('register_check/', views.register_check),
    path('login/', views.login, name='login'),
    path('personal_information/',views.personal_information,name='personal_information'),
    path('address/',views.address,name='address'),
    path('address/address_change/',views.address_change,name='address_change'),
    path('logout/',views.logout,name='logout'),




]
