#!/usr/bin/python3
'''Status of your API'''
from api.v1.views import app_views as views
from flask import Flask, jsonify as json, request, abort
from models import storage
from models.place import Place


@views.route('/places', methods=['GET'], strict_slashes=False)
def getPlace():
    """Retrieves list all Place"""
    places = [place.to_dict()
              for place in storage.all(Place).values()]
    return json(places)


@views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getPlace(place_id):
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


@views.route('/places', methods=['POST'], strict_slashes=False)
def create_place():
    """Creates new Place"""
    data = request.get_json()
    if data is None:
        return json({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return json({"error": "Missing name"}), 400
    new_place = Place(**data)
    new_place.save()
    return json(new_place.to_dict()), 201


@views.route('/places/<place_id>', methods=['PUT'],
             strict_slashes=False)
def new_place(place_id):
    """Updates Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return json({"error": "Not a JSON"}), 400
    keys = ['id', 'created_at', 'updated_at']
    for ky, val in data.items():
        if ky not in keys:
            setattr(place, ky, val)
    place.save()
    return json(place.to_dict())
