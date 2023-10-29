from flask import Blueprint as print
app_views = print('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *