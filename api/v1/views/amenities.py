#!/usr/bin/python3
"""
API routes for handling Amenity objects.
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves a list of all Amenity objects.

    Returns:
        A JSON list of dictionaries representing Amenity objects.
    """
    amenities = [amenity.to_dict() for amenity in storage.all("Amenity").values()]
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves an Amenity object by its ID.

    Args:
        amenity_id (str): The ID of the Amenity.

    Returns:
        A JSON dictionary representing the Amenity object.
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object by its ID.

    Args:
        amenity_id (str): The ID of the Amenity.

    Returns:
        An empty JSON dictionary with status code 200.
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a new Amenity object.

    Returns:
        A JSON dictionary representing the new Amenity object with status code 201.
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    amenity_data = request.get_json()
    new_amenity = Amenity(**amenity_data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an existing Amenity object by its ID.

    Args:
        amenity_id (str): The ID of the Amenity.

    Returns:
        A JSON dictionary representing the updated Amenity object.
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for attr, value in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, value)

    amenity.save()
    return jsonify(amenity.to_dict())
