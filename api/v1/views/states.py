#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views as views
from models import storage
from models.state import State
from flask import jsonify as json, abort, request


@views.route("/states", strict_slashes=False, methods=["GET"])
@views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def states(state_id=None):
    """show states and states with id"""
    list_s = []
    if state_id is None:
        objs = storage.all(State).values()
        for val in objs:
            list_s.append(val.to_dict())
        return json(list_s)
    else:
        result = storage.get(State, state_id)
        if result is None:
            abort(404)
        return json(result.to_dict())


@views.route("/states/<state_id>", strict_slashes=False,
             methods=["DELETE"])
def delete(state_id):
    """delete method"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return json({}), 200


@views.route("/states", strict_slashes=False, methods=["POST"])
def create():
    """create a new post req"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return json(new_state.to_dict()), 201


@views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update(state_id):
    """update state"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return json(obj.to_dict()), 200
