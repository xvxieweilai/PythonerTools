#!/usr/bin/env python
# encoding: utf-8


"""
@author: XXWL
@contact: xxwl@duee.cn
@file: ${NAME}.py
@time: ${DATE} ${TIME}
@desc:
"""

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
