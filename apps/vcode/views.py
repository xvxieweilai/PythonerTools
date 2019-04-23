from django.shortcuts import render

# Create your views here.
from django.views import View
from utils.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse

VCODE_EXPIRES = 60 * 5


class VcodeView(View):
    def get(self, request, uuid):
        text, code, image = captcha.generate_captcha()
        redis_cli = get_redis_connection('image_code')
        redis_cli.setex(str(uuid), VCODE_EXPIRES, code)
        return HttpResponse(image, content_type='image/png')
