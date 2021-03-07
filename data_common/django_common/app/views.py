# from django.shortcuts import render
import json
from django.db import connection
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from data_common.django_common import get_request_args
from data_common.utils.log_util import Logger
from data_common.django_common.utils.mysql_util import DjangoSqlUtil

# Create your views here.
@csrf_exempt
def get_test(request):
    cursor = connection.cursor()
    cursor.execute('SHOW TABLES')
    results = cursor.fetchall()
    desc = cursor.description
    keys = [col[0] for col in desc]
    data_list = []
    for result in results:
        result = dict(zip(keys, list(result)))
        data_list.append(result)
        Logger.info(f'result: {result}')
    return HttpResponse(json.dumps({'data': data_list}))


@csrf_exempt
def get_test2(request):
    try:
        """直接执行sql操作"""
        args = get_request_args(request)
        sql = args.get('sql')
        Logger.info(request)
        db = DjangoSqlUtil()
        data_list = db.command(sql)
        return HttpResponse(json.dumps({'data': data_list, 'total': len(data_list)}))
    except Exception as e:
        return HttpResponse(json.dumps({'data': [], 'total': 0, 'msg': str(e)}))


@csrf_exempt
def get_test3(request):
    try:
        """插入值操作"""
        args = get_request_args(request)
        data = args.get('data')
        data = data if isinstance(data, list) else [data]
        Logger.info(request)
        db = DjangoSqlUtil()
        total = db.insert('user', data)
        return HttpResponse(json.dumps({'data': [], 'total': total}))
    except Exception as e:
        return HttpResponse(json.dumps({'data': [], 'total': 0, 'msg': str(e)}))


@csrf_exempt
def get_test4(request):
    try:
        """更新操作"""
        args = get_request_args(request)
        Logger.info(request)
        db = DjangoSqlUtil()
        total = db.update('user', update={'age': 30},  where={'name': 'Tom0922'})
        return HttpResponse(json.dumps({'data': [], 'total': total}))
    except Exception as e:
        return HttpResponse(json.dumps({'data': [], 'total': 0, 'msg': str(e)}))