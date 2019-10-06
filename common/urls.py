"""teamproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from common.views import send_sms_code, get_captcha, get_qrcode

urlpatterns = [
    path('qrcode/', get_qrcode, name='qrcode'),
    path('captcha/', get_captcha, name='captcha'),
    path('mobile_code/<str:tel>/', send_sms_code, name='mobile_code'),
]
