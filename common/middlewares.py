import re

from django.core.cache import caches
from django.http import JsonResponse

TEL_PATTERN = re.compile(r'/common/mobile_code/(?P<tel>1[3-9]\d{9})/')


def block_sms_middleware(get_response):

    def middleware(request, *args, **kwargs):
        url = request.path
        if url.startswith('/common/mobile_code'):
            matcher = TEL_PATTERN.fullmatch(url)
            if matcher:
                tel = matcher.group('tel')
                if caches['default'].get(tel):
                    return JsonResponse({
                        'code': 10002,
                        'msg': '请不要在60秒以内重复发送手机验证码'
                    })
            else:
                return JsonResponse({
                    'code': 10003,
                    'msg': '请提供有效的手机号'
                })
        return get_response(request)

    return middleware
