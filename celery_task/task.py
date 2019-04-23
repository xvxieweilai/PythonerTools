#!/usr/bin/env python
# encoding: utf-8


"""
@author: XXWL
@contact: xxwl@duee.cn
@file: task.py
@time: 2019-04-23 23:21
@desc:
"""
import os
import zipfile

import git
from django_redis import get_redis_connection

from celery_task.main import app


def zipDir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    zip = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip.close()


class Progress(git.remote.RemoteProgress):

    def set_key(self, task_):
        self.task_ = task_

    def update(self, op_code, cur_count, max_count=None, message=''):
        redis_cli = get_redis_connection("task_list")
        redis_cli.set(self.task_, '%s, %s, %s, %s' % (op_code, cur_count, max_count, message))
        print('%s, %s, %s, %s' % (op_code, cur_count, max_count, message))


@app.task(bind=True, name='git_clone', retry_backoff=3, max_retries=3, time_limit=1800)
def git_clone(self, git_url):
    print(git_url)
    if git_url.endswith(".git"):
        _url = git_url[git_url.rfind("/"):git_url.rfind(".")]
    else:
        _url = git_url[git_url.rfind("/")]
    progress = Progress()
    progress.set_key(git_clone.request.id)
    repo = git.Repo.clone_from(git_url, "/tmp/" + git_clone.request.id + _url,
                               progress=progress)
    zipDir("/tmp/" + git_clone.request.id, "/tmp/" + git_clone.request.id + ".zip")
    redis_cli = get_redis_connection("task_list")
    redis_cli.set(git_clone.request.id, 'finished')
