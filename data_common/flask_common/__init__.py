# coding=utf-8
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={"*": {"origins": "*"}})

# 一般
from data_common.flask_common import flask_test
# 蓝图
from data_common.flask_common.admin import admin
from data_common.flask_common.web import web
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(web, url_prefix='/web')

