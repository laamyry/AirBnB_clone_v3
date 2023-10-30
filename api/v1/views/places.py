#!/usr/bin/python3
'''Status of your API'''
from api.v1.views import app_views as views
from flask import Flask, jsonify as json, request, abort
from models import storage
from models.place import Place
from models.user import User
from models.city import City


@views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def getCityPlace(city_id):
    """Retrieves list of all Places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return json(places)


@views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getPlace(place_id):
    """Retrieves Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return json(place.to_dict())


@views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def deletePlace(place_id):
    """Deletes Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return json({})


@views.route('/cities/<city_id>/places', methods=['POST'],
             strict_slashes=False)
def createPlace(city_id):
    """Creates new Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return json({"error": "Not a JSON"}), 400
    if 'user_id' not in data:
        return json({"error": "Missing user_id"}), 400
    if storage.get(User, data['user_id']) is None:
        abort(404)
    if 'name' not in data:
        return json({"error": "Missing name"}), 400

    nPlace = Place(**data)
    nPlace.city_id = city.id
    nPlace.save()
    return json(nPlace.to_dict()), 201


@views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updatePlace(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return json({"error": "Not a JSON"}), 400
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return json(place.to_dict())
