#!/usr/bin/env python
# encoding: utf-8


"""
@author: XXWL
@contact: xxwl@duee.cn
@file: main.py
@time: 2019-04-23 23:21
@desc:
"""
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PythonerTools.settings')
app = Celery('git_task')
app.config_from_object('celery_task.config')
app.autodiscover_tasks([
    'celery_task.git_clone',
])
