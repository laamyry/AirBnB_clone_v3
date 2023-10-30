#!/usr/bin/python3
'''Status of your API'''
from api.v1.views import app_views as views
from flask import jsonify as json
from models import storage


@views.route('/status', methods=['GET'], strict_slashes=False)
def getstatus():
    """status"""
    return json({"status": "OK"})


@views.route('/stats', methods=['GET'], strict_slashes=False)
def getstats():
    """stats"""
    counter = storage.count
    amen = counter("Amenity")
    citi = counter("City")
    plac = counter("Place")
    revi = counter("Review")
    stat = counter("State")
    user = counter("User")

    stats = {
        "amenities": amen,
        "cities": citi,
        "places": plac,
        "reviews": revi,
        "states": stat,
        "users": user}

    return json(stats)
