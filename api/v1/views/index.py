#!/usr/bin/python3
'''Status of your API'''
from api.v1.views import app_views as views
from flask import jsonify as json
from models import storage


@views.route('/status', methods=['GET'], strict_slashes=False)
def getstatus():
    """status"""
    return json({"status": "OK"})

@views.route('stats', methods=['GET'])
def getstats():
    """stats"""
    amen = storage.count("Amenity")
    citi = storage.count("City")
    plac = storage.count("Place")
    revi = storage.count("Review")
    stat = storage.count("State")
    user = storage.count("User")

    stats = {
        "amenities": amen, "cities": citi,
        "places": plac, "reviews": revi,
        "states": stat, "users": user}

    return json(stats)
