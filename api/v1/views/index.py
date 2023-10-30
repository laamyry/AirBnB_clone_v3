#!/usr/bin/python3
'''Status of your API'''
from api.v1.views import app_views as views
from flask import jsonify as json


@views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """status"""
    return json({"status": "OK"})
