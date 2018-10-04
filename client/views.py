from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from django.template import loader
# Create your views here.


def index(request):
    """
    操盘手默认界面
    :param request:
    :return:
    """
    # template = loader.get_template('client/index.html')
    # return HttpResponse(template.render(None,request))
    return render(request, 'client/index.html', None)
    # return HttpResponse("hello ,world, this is client")


@csrf_exempt
def login(request):
    """
    操盘手登陆转发
    :param request:
    :return:
    """
    if request.method =='POST':
        username = request.POST.get('user', None)
        pwd = request.POST.get('pwd', None)
        user = User.objects.filter(username=username).filter(pwd=pwd)
        if len(user) > 0:
            return render(request, 'client/loginindex.html', None)
    # 登陆失败或者非post请求则返回首页
    return render(request, 'client/index.html', None)


def order_index(request):
    """
     操盘手登陆界面
    :param request:
    :return:
    """

    return HttpResponse("hello , welcome")


def order(request):
    """
    操盘手下单操作
    :param request:
    :return:
    """
    return HttpResponse("hello , ordering----")