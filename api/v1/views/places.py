#!/usr/bin/python3
"""
Module for managing places.
"""
from api.v1.views import (app_views, Place, storage)
from flask import (abort, jsonify, request)
import os


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_in_city(city_id):
    """Retrieve all places in a specified city.

    Args:
        city_id (str): The ID of the city.

    Returns:
        JSON: List of places in the specified city.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_json() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieve a place by its ID.

    Args:
        place_id (str): The ID of the place.

    Returns:
        JSON: Details of the specified place.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_json())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a place by its ID.

    Args:
        place_id (str): The ID of the place.

    Returns:
        JSON: Empty dictionary on successful deletion.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Create a new place in a specified city.

    Args:
        city_id (str): The ID of the city.

    Returns:
        JSON: Details of the newly created place.
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        return "Not a JSON", 400
    if 'user_id' not in data:
        return "Missing user_id", 400
    user = storage.get("User", data.get("user_id"))
    if user is None:
        abort(404)
    if 'name' not in data:
        return "Missing name", 400
    data["city_id"] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_json()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Update an existing place.

    Args:
        place_id (str): The ID of the place to update.

    Returns:
        JSON: Details of the updated place.
    """
    data = request.get_json()
    if not data:
        return "Not a JSON", 400
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    for key in ("id", "user_id", "city_id", "created_at", "updated_at"):
        data.pop(key, None)
    for key, value in data.items():
        setattr(place, key, value)
    place.save()
    return jsonify(place.to_json()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Search for places based on filters.

    Returns:
        JSON: List of places matching the search criteria.
    """
    data = request.get_json()
    if not data:
        return "Not a JSON", 400
    
    city_ids = data.get("cities", [])
    state_ids = data.get("states", [])
    amenities_ids = data.get("amenities", [])

    if state_ids:
        states = [storage.get("State", state_id) for state_id in state_ids]
        city_ids.extend([city.id for state in states if state for city in state.cities])
    
    city_ids = list(set(city_ids))
    
    all_places = storage.all("Place").values()
    
    if city_ids:
        all_places = [place for place in all_places if place.city_id in city_ids]
    
    if amenities_ids:
        if os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':
            all_places = [place for place in all_places if set(amenities_ids).issubset(set(place.amenities_id))]
        else:
            all_places = [place for place in all_places if all(amenity in [a.id for a in place.amenities] for amenity in amenities_ids)]
    
    return jsonify([place.to_json() for place in all_places])

