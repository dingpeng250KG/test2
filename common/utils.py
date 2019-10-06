"""
项目常用工具函数
"""
import http
import json
import random

from hashlib import md5
from io import BytesIO
from urllib.error import URLError
from urllib.parse import urlencode

import qrcode
import requests
from qiniu import Auth, put_file, put_stream

from teamproject import app


def get_ip_address(request):
    """获得请求的IP地址"""
    ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
    return ip or request.META['REMOTE_ADDR']


def to_md5_hex(origin_str):
    """生成MD5摘要"""
    return md5(origin_str.encode('utf-8')).hexdigest()


ALL_NUMS = '0123456789'


def gen_mobile_code(length=6):
    """生成指定长度的手机验证码"""
    return ''.join(random.choices(ALL_NUMS, k=length))


ALL_CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def gen_captcha_text(length=4):
    """生成指定长度的图片验证码文字"""
    return ''.join(random.choices(ALL_CHARS, k=length))


def gen_qrcode(data):
    """生成二维码"""
    image = qrcode.make(data)
    buffer = BytesIO()
    image.save(buffer)
    return buffer.getvalue()


SMS_SERVER = '106.ihuyi.com'
SMS_URL = '/webservice/sms.php?method=Submit'
SMS_ACCOUNT = 'C64404338'
SMS_PASSWORD = '26384b1d8223ee8000737673dd5ef40d'
MSG_TEMPLATE = '您的验证码是：%s。请不要把验证码泄露给其他人。'


@app.task
def send_sms_by_ihuyi(tel, code):
    """发送短信（调用互亿无线短信网关）"""
    params = urlencode({
        'account': SMS_ACCOUNT,
        'password': SMS_PASSWORD,
        'content': MSG_TEMPLATE % code,
        'mobile': tel,
        'format': 'json'
    })
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/plain'
    }
    conn = http.client.HTTPConnection(SMS_SERVER, port=80, timeout=10)
    try:
        conn.request('POST', SMS_URL, params, headers)
        return conn.getresponse().read().decode('utf-8')
    except URLError or KeyError as e:
        return json.dumps({
            'code': 10004,
            'msg': '短信服务暂时无法使用'
        })
    finally:
        conn.close()


@app.task
def send_sms_by_luosimao(tel, mobile_code):
    """发送短信验证码（调用螺丝帽短信网关）"""
    resp = requests.post(
        url='http://sms-api.luosimao.com/v1/send.json',
        auth=('api', 'key-524049379b633f7a4344494e95b09f89'),
        data={
            'mobile': tel,
            'message': f'您的验证码为{mobile_code}。【铁壳测试】'
        },
        timeout=10,
        verify=False)
    return resp.content


QINIU_ACCESS_KEY = 'KarvlHfUdoG1mZNSfDVS5Vh3nae2jUZumTBHK-PR'
QINIU_SECRET_KEY = 'SFPFkAn5NENhdCMqMe9wd_lxGHAeFR5caXxPTtt7'
QINIU_BUCKET_NAME = 'teamproject'

auth = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)


@app.task
def upload_filepath_to_qiniu(file_path, filename):
    """将文件上传到七牛云存储"""
    token = auth.upload_token(QINIU_BUCKET_NAME, filename)
    put_file(token, filename, file_path)


@app.task
def upload_stream_to_qiniu(file_stream, filename, size):
    """将文件上传到七牛云存储"""
    token = auth.upload_token(QINIU_BUCKET_NAME, filename)
    put_stream(token, filename, file_stream, None, size)
