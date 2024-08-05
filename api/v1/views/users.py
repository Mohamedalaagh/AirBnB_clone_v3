#!/usr/bin/python3
"""
API routes for handling User objects.
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves a list of all User objects.

    Returns:
        A JSON list of dictionaries representing User objects.
    """
    users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object by its ID.

    Args:
        user_id (str): The ID of the User.

    Returns:
        A JSON dictionary representing the User object.
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object by its ID.

    Args:
        user_id (str): The ID of the User.

    Returns:
        An empty JSON dictionary with status code 200.
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new User object.

    Returns:
        A JSON dictionary representing the new User object with status code 201.
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    user_data = request.get_json()
    if 'email' not in user_data:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in user_data:
        return make_response(jsonify({'error': 'Missing password'}), 400)

    new_user = User(**user_data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates an existing User object by its ID.

    Args:
        user_id (str): The ID of the User.

    Returns:
        A JSON dictionary representing the updated User object.
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for attribute, value in request.get_json().items():
        if attribute not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attribute, value)

    user.save()
    return jsonify(user.to_dict())
