# coding=utf-8
from data_common.flask_common import app
from flask import request, jsonify


# request.args.get("key")    # 获取get请求参数
# request.form.get("key")    # 获取form表单数据
# request.get_json()         # 获取post请求非form参数
# request.values.get("key")  # 获取所有参数:get请求参数, form表单数据, 但不包括非form参数


@app.route('/get_test/', methods=['GET'])
def get_test():
    args = request.args
    user = args.get('user')
    return jsonify({'args': args, 'user': user})


@app.route('/form_test/', methods=['POST'])
def form_test():
    args = request.form
    user = args.get('user')
    return jsonify({'args': args, 'user': user})


@app.route('/post_test/', methods=['POST'])
def post_test():
    args = request.get_json()
    user = args.get('user')
    return jsonify({'args': args, 'user': user})