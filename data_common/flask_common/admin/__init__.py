# -*- coding:utf-8 -*-
import os
from flask import Blueprint

admin = Blueprint(
    'admin',
    __name__,
    template_folder=os.path.dirname(__file__) + '/templates',
    static_folder=os.path.dirname(__file__) + 'static'
)
from data_common.flask_common.admin import views