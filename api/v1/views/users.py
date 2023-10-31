#!/usr/bin/python3
'''Status of your API'''
from api.v1.views import app_views as views
from flask import Flask, jsonify as json, request, abort
from models import storage
from models.user import User
from models.city import City


@views.route('/users', methods=['GET'], strict_slashes=False)
def getUsers():
    """Retrieves list of all User"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return json(users)


@views.route('/users/<user_id>', methods=['GET'],
             strict_slashes=False)
def getUser(user_id):
    """Retrieves a User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return json(user.to_dict())


@views.route('/users/<user_id>', methods=['DELETE'],
             strict_slashes=False)
def deleteUser(user_id):
    """Deletes User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return json({})


@views.route('/users', methods=['POST'], strict_slashes=False)
def createUser():
    """Creates new User"""
    data = request.get_json()
    if data is None:
        return json({"error": "Not a JSON"}), 400
    if 'email' not in data:
        return json({"error": "Missing email"}), 400
    if 'password' not in data:
        return json({"error": "Missing password"}), 400

    nUser = User(**data)
    nUser.save()
    return json(nUser.to_dict()), 201


@views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updateUser(user_id):
    """Updates User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return json({"error": "Not a JSON"}), 400
    keys = ['id', 'email', 'created_at', 'updated_at']
    for ky, val in data.items():
        if ky not in keys:
            setattr(user, ky, val)
    user.save()
    return json(user.to_dict())
