from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
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


def loginindex(request):
    """
    登陆成功首页
    :param request:
    :return:
    """
    return render(request, 'client/loginindex.html', None)


def order_index(request):
    """
     操盘手登陆界面
    :param request:
    :return:
    """

    return render(request, 'client/orderindex.html', None)

@csrf_exempt
def order(request):
    """
    操盘手下单操作
    :param request:
    :return:
    """
    params = []
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        # print(body)
        # print(body)
        datas = json.loads(body)
        # print(datas)
        product = str(datas['product'])
        # print(product)
        amount = str(datas['amount'])
        price = str(datas['price'])
        params.append(product)
        params.append(amount)
        params.append(price)
        return HttpResponse(content=json.dumps(params), content_type='application/json;charset = utf-8',
                        status='200',
                        reason='success',
                        charset='utf-8')
    # return HttpResponse("hello ,world, this is client")

