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
from django.conf import settings
from django.urls import path, include

from common.views import echarts, home, to_login, to_register, to_logout, to_publish

urlpatterns = [
    path('', home, name='home'),
    path('to_login/', to_login, name='to_login'),
    path('to_register/', to_register, name='to_register'),
    path('to_logout/', to_logout, name='to_logout'),
    path('to_publish/', to_publish, name='to_publish'),
    path('echarts/', echarts, name='echarts'),
    path('api/', include('api.urls')),
    path('backend/', include('backend.urls')),
    path('common/', include('common.urls')),
]

if settings.DEBUG:

    import debug_toolbar

    urlpatterns.insert(0, path('__debug__/', include(debug_toolbar.urls)))
