from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='regster'),
    path('register_check/', views.register_check),
    path('login/', views.login, name='login')

]
