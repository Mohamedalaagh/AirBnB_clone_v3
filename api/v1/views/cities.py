#!/usr/bin/python3
"""
API routes for handling City objects.
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """
    Retrieves a list of all City objects in a specified State.

    Args:
        state_id (str): The ID of the State.

    Returns:
        A JSON list of dictionaries representing City objects.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object by its ID.

    Args:
        city_id (str): The ID of the City.

    Returns:
        A JSON dictionary representing the City object.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object by its ID.

    Args:
        city_id (str): The ID of the City.

    Returns:
        An empty JSON dictionary with status code 200.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    Creates a new City object in a specified State.

    Args:
        state_id (str): The ID of the State.

    Returns:
        A JSON dictionary representing the new City object with status code 201.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)

    city_data = request.get_json()
    city_data['state_id'] = state_id
    new_city = City(**city_data)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    Updates an existing City object by its ID.

    Args:
        city_id (str): The ID of the City.

    Returns:
        A JSON dictionary representing the updated City object.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for attr, value in request.get_json().items():
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, attr, value)

    city.save()
    return jsonify(city.to_dict())

