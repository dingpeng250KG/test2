from django.core.cache import caches
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from api.serializers import HouseInfoSerializer
from common.captcha import Captcha
from common.models import HouseInfo
from common.utils import gen_mobile_code, send_sms_by_ihuyi, gen_captcha_text, gen_qrcode


def home(request):
    queryset = HouseInfo.objects.all() \
        .select_related('type', 'district', 'estate', 'agent') \
        .prefetch_related('tags').order_by('-pubdate')[:5]
    serializer = HouseInfoSerializer(queryset, many=True)
    return render(request, 'index.html', context={'results': serializer.data})


def to_login(request):
    return render(request, 'login.html', context={})


def to_register(request):
    return render(request, 'register.html', context={})


def to_logout(request):
    request.session.flush()
    return redirect('/')


def to_publish(request):
    return render(request, 'publish.html', context={})


def echarts(request):
    """报表"""
    return render(request, 'echarts.html')


def get_qrcode(request):
    """获取二维码"""
    url = request.GET.get('url', 'https://jackfrued.xyz')
    image = gen_qrcode(url.encode())
    return HttpResponse(image, content_type='image/png')


def get_captcha(request):
    """获取图片验证码"""
    captcha_code = gen_captcha_text()
    request.session['captcha_code'] = captcha_code
    image = Captcha.instance().generate(captcha_code)
    return HttpResponse(image, content_type='image/png')


def send_sms_code(request, tel):
    """发送短信验证码"""
    mobile_code = gen_mobile_code()
    request.session['mobile_code'] = mobile_code
    # 通过delay方法来调用该函数相当于是生产者生产一个任务放到消息队列中
    # 如果要处理这个任务还需要启动消费者，启动消费者的命令如下所示：
    # celery -A teamproject worker -l debug
    # 如果在Windows平台下使用celery 4.x版本需要先安装eventlet作为辅助
    # pip install eventlet
    # 然后启动celery消费者的时候需要加一个参数，如下所示：
    # celery -A common.utils worker -l info -P eventlet
    send_sms_by_ihuyi.delay(tel, mobile_code)
    caches['default'].set(tel, mobile_code, timeout=60)
    return JsonResponse({
        'code': 10001,
        'msg': '短信验证码发送成功'
    })
