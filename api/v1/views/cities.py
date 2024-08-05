#!/usr/bin/python3
"""
This module defines API endpoints related to cities.
"""
from api.v1.views import app_views, City, storage
from flask import abort, jsonify, request

@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def state_all_cities(state_id):
    """Retrieve all cities of a given state by its ID.
    
    Args:
        state_id (str): The ID of the state.
        
    Returns:
        Response: JSON response containing a list of all city objects for the given state.
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    all_cities = [city.to_json() for city in state.cities]
    return jsonify(all_cities)

@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def one_city(city_id):
    """Retrieve a city by its ID.
    
    Args:
        city_id (str): The ID of the city to retrieve.
        
    Returns:
        Response: JSON response containing the city object if found, else 404 error.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())

@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_one_city(city_id):
    """Delete a city by its ID.
    
    Args:
        city_id (str): The ID of the city to delete.
        
    Returns:
        Response: JSON response with an empty dictionary and status code 200 if successful, else 404 error.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return jsonify({})

@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_one_city(state_id):
    """Create a new city associated with a given state.
    
    Args:
        state_id (str): The ID of the state.
        
    Returns:
        Response: JSON response containing the new city object if successful, else 400 or 404 error.
    """
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    if 'name' not in r.keys():
        return "Missing name", 400
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    c = City(**r)
    c.state_id = state_id
    c.save()
    return jsonify(c.to_json()), 201

@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_one_city(city_id):
    """Update an existing city by its ID.
    
    Args:
        city_id (str): The ID of the city to update.
        
    Returns:
        Response: JSON response containing the updated city object if successful, else 400 or 404 error.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    try:
        r = request.get_json()
    except:
        r = None
    if r is None:
        return "Not a JSON", 400
    for k in ("id", "created_at", "updated_at", "state_id"):
        r.pop(k, None)
    for k, v in r.items():
        setattr(city, k, v)
    city.save()
    return jsonify(city.to_json()), 200

