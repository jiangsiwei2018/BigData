# coding=utf-8
import os
import json
django_path = os.path.dirname(__file__)


def get_request_args(request, upload_file=False):
    args = {}
    files = {}
    if request.method == 'GET' and request.GET:
        args = request.GET
    elif request.method == 'POST' and request.POST:
        args = request.POST
        files = request.FILES
    elif request.method == 'POST' and request.body:
        args = json.loads(str(request.body, encoding='utf-8'))
    if upload_file:
        return args, files
    return args


# 数据库必须配置
# import pymysql
# pymysql.version_info = (1, 4, 0, "final", 0)
# pymysql.install_as_MySQLdb()