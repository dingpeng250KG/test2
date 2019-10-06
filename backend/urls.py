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

from backend.views import download, export_excel, export_pdf, get_bar_data

urlpatterns = [
    path('download/', download, name='download'),
    path('excel/', export_excel, name='excel'),
    path('pdf/', export_pdf, name='pdf'),
    path('bar_data/', get_bar_data, name='bar_data'),
]
