#!/usr/bin/env python
# encoding: utf-8


"""
@author: XXWL
@contact: xxwl@duee.cn
@file: urls.py
@time: 2019-04-23 20:53
@desc:
"""

from django.urls import path, include
from . import views

app_name = 'vcode'
urlpatterns = [
    path('<uuid:uuid>/', views.VcodeView.as_view(), name='index'),
]
