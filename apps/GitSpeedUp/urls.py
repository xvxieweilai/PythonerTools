#!/usr/bin/env python
# encoding: utf-8


"""
@author: XXWL
@contact: xxwl@duee.cn
@file: urls.py
@time: 2019-04-23 19:01
@desc:
"""

from django.urls import path, include
from . import views

app_name = 'git'
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.GitSpeedUpView.as_view(), name='index'),
    path('DownProcess/<uuid:uuid>/', views.GitDownLoadFileView.as_view(), name='process'),
    path('FileDown/<uuid:uuid>/', views.FileDownView.as_view(), name='filedown'),

]
