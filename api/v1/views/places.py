#!/usr/bin/python3
'''Status of your API'''
from api.v1.views import app_views as views
from flask import Flask, jsonify as json, request, abort
from models import storage
from models.place import Place
from models.user import User
from models.city import City


@views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_city_places(city_id):
    """Retrieves list of all Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return json(places)


@views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return json(place.to_dict())


@views.route('/places/<place_id>', methods=['DELETE'],
             strict_slashes=False)
def delete_place(place_id):
    """Deletes Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return json({})


@views.route('/cities/<city_id>/places', methods=['POST'],
             strict_slashes=False)
def create_place(city_id):
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

    new_place = Place(**data)
    new_place.city_id = city.id
    new_place.save()
    return json(new_place.to_dict()), 201


@views.route('/places/<place_id>', methods=['PUT'],
             strict_slashes=False)
def update_place(place_id):
    """Updates Place"""
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
