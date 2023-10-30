#!/usr/bin/python3
'''Status of your API'''
from api.v1.views import app_views as views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify as json, request, abort


@views.route("/states/<state_id>/cities", strict_slashes=False,
             methods=["GET"])
def cities(state_id):
    """show cities"""
    list_c = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    for city in cities:
        list_c.append(city.to_dict())
    return json(list_c)


@views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def cities_id(city_id):
    """Retrieves City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return json(city.to_dict())


@views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete(city_id):
    """delete method"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return json({}), 200


@views.route("/states/<state_id>/cities", strict_slashes=False,
             methods=["POST"])
def create(state_id):
    """create post"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = City(state_id=state.id, **data)
    new_state.save()
    return json(new_state.to_dict()), 201


@views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update(city_id):
    """update city"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return json(obj.to_dict()), 200
