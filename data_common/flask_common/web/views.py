# -*- coding:utf-8 -*-
from data_common.flask_common.web import web
from flask import render_template,request


@web.route('/index/')
def index():
    return render_template('index.html')


@web.route('/search/')
def search():
    args = request.args  # get请求，打印url后面所有的参数（key:value形式），如果有多个参数，通过request.args.get('key')的方式获取值
    print(args)
    return render_template('search.html')


@web.route('/login/', methods=['POST','GET'])
def login():
    if request.method == 'GET':  # 此处判断get和post方法与django相同
        return render_template('login.html')
    else:
        username = request.form.get('username')  #post请求。获取模版语言中输入框输入的值
        password = request.form.get('password')
        return "post request, username: %s password:%s" % (username,password)