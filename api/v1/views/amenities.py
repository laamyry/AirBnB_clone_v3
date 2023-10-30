#!/usr/bin/python3
'''Status of your API'''
from api.v1.views import app_views as views
from flask import Flask, jsonify as json, request, abort
from models import storage
from models.amenity import Amenity


@views.route('/amenities', methods=['GET'], strict_slashes=False)
def getAmenities():
    """Retrieves list all Amenity"""
    amenities = [amenity.to_dict()
                 for amenity in storage.all(Amenity).values()]
    return json(amenities)


@views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def getAamenity(amenity_id):
    """Retrieves Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return json(amenity.to_dict())


@views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return json({})


@views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates new Amenity"""
    data = request.get_json()
    if data is None:
        return json({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return json({"error": "Missing name"}), 400
    new_amenity = Amenity(**data)
    new_amenity.save()
    return json(new_amenity.to_dict()), 201


@views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return json({"error": "Not a JSON"}), 400
    keys = ['id', 'created_at', 'updated_at']
    for ky, val in data.items():
        if ky not in keys:
            setattr(amenity, ky, val)
    amenity.save()
    return json(amenity.to_dict())
