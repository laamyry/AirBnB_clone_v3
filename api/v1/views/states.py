#!/usr/bin/python3
'''Status of your API'''
from api.v1.views import app_views as views
from flask import Flask, jsonify as json, abort, request
from models import storage
from models.state import State


@views.route('/status')
def states():
    """get states"""
    states = [state.to_dict() for state in storage.all("State").values()]

    return json(states)


@views.route('/states/<state_id>', methods=['GET'])
def state(state_id):
    """get stat"""
    state = storage.get("State", state_id)
    dic = state.to_dict()
    if state is None:
        abort(404)
    return json(dic)


@views.route('/states/<state_id>', methods=['DELETE'])
def delete(state_id):
    """delete state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return json({})


@views.route('/states', methods=['GET'])
def create():
    """create state"""
    data = request.get_json()
    if data is None:
        return json({"error": "Not a JSON"}, 400)
    if "name" not in data:
        return json({"error": "Missing name"}, 400)
    nState = State(**data)
    nState.save()
    return json(nState.to_dict(), 201)


@views.route('/states/<state_id>', methods=['POST'])
def update(state_id):
    """update state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return json({"error": "Not a JSON"}, 400)
    kys = ["id", "created_at", "updated_at"]
    for ky, val in data.items():
        if ky not in kys:
            setattr(state, ky, val)
    state.save()
    return json(state.to_dict())
