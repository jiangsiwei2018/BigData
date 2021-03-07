# -*- coding:utf-8 -*-
from data_common.flask_common.admin import admin


@admin.route('/index/')
def index():
    return 'Admin.Index'