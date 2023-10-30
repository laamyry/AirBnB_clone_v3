#!/usr/bin/python3
'''Status of your API'''
from flask import Blueprint as bprint
app_views = bprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *
from api.v1.views.states import *
