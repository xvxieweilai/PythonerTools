from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import *
from django_redis import get_redis_connection
from celery_task.task import git_clone


class GitSpeedUpView(View):
    def return_error_message(self, req, error_message):
        return render(req, 'GitSpeedUp/index.html', {"error_message": error_message})

    def get_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
        return ip

    def get(self, request):
        return self.return_error_message(request, "")

    def post(self, request):
        user_ip = self.get_ip(request)
        giturl = request.POST.get('giturl')
        uuid = request.POST.get('uuid')
        vcode = request.POST.get('vcode')
        if not all([giturl, uuid, vcode]):
            return self.return_error_message(request, "输入不完整")
        redis_cli = get_redis_connection("image_code")
        redis_v_code = redis_cli.get(uuid)
        if redis_v_code and redis_v_code.decode().upper() == vcode.upper():
            redis_cli.delete(uuid)
            redis_cli = get_redis_connection('default')
            if not redis_cli.get("user_" + user_ip):
                redis_cli.setex("user_" + user_ip, 60, "_flag")
            else:
                return self.return_error_message(request, "请求频率过高 稍等1分钟")
            if not giturl.startswith("http://"):
                return self.return_error_message(request, "请输入http地址 暂不支持git")

            task = git_clone.delay(giturl)
            return render(request, 'GitSpeedUp/download.html', {"task_id": task})
        else:
            return render(request, 'GitSpeedUp/index.html', {"error_message": "验证码输入错误"})


class GitDownLoadFileView(View):
    def get(self, request, uuid):
        redis_cli = get_redis_connection("task_list")
        message = redis_cli.get(str(uuid))
        if message:
            return JsonResponse({"message": message.decode()})
        return JsonResponse({"message": "队列中"})


class FileDownView(View):
    def get(self, request, uuid):
        redis_cli = get_redis_connection("task_list")
        message = redis_cli.delete(str(uuid))
        file = open('/tmp/' + str(uuid) + '.zip', 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="' + str(uuid) + '.zip"'
        return response
