# coding=utf-8
# __project__ = " "
# __author__ = "Nicksphere"
# __time__ = "2018/10/1 下午5:08"


from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('orderindex', views.order_index, name='order_index'),
    path('order', views.order, name='order'),
    path('login', views.login, name='login'),
    path('loginindex', views.loginindex, name='loginindex')
]