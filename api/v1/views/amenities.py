#!/usr/bin/python3
"""
This module handles operations related to amenities.
"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import (abort, jsonify, request)

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenities(amenity_id=None):
    """
    Retrieves amenities information.

    If amenity_id is not provided, returns a list of all amenities.
    If amenity_id is provided, returns the amenity with the specified ID.

    Parameters:
      - name: amenity_id
        in: path
        type: string
        description: The ID of the amenity to retrieve. If not provided, returns all amenities.
        required: false
        example: "cf701d1a-3c19-4bac-bd99-15321f1140f2"

    Responses:
      200:
        description: A list of amenities or a single amenity object
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Amenity'
            examples:
              single:
                value: {
                  "__class__": "Amenity",
                  "created_at": "2017-03-25T02:17:06",
                  "id": "cf701d1a-3c19-4bac-bd99-15321f1140f2",
                  "name": "Dog(s)",
                  "updated_at": "2017-03-25T02:17:06"
                }
              list:
                value: [
                  {
                    "__class__": "Amenity",
                    "created_at": "2017-03-25T02:17:06",
                    "id": "cf701d1a-3c19-4bac-bd99-15321f1140f2",
                    "name": "Dog(s)",
                    "updated_at": "2017-03-25T02:17:06"
                  }
                ]
    """
    if amenity_id is None:
        amenities = [amenity.to_json() for amenity in storage.all("Amenity").values()]
        return jsonify(amenities)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_json())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a specified amenity.

    Parameters:
      - name: amenity_id
        in: path
        type: string
        description: The ID of the amenity to delete.
        required: true
        example: "cf701d1a-3c19-4bac-bd99-15321f1140f2"

    Responses:
      200:
        description: Confirmation of deletion
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Amenity deleted successfully"
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a new amenity.

    Request body should be a JSON object with the following fields:
      - name: string (required)

    Responses:
      201:
        description: The created amenity
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Amenity'
            examples:
              value: {
                "__class__": "Amenity",
                "created_at": "2017-03-25T02:17:06",
                "id": "cf701d1a-3c19-4bac-bd99-15321f1140f2",
                "name": "Dog(s)",
                "updated_at": "2017-03-25T02:17:06"
              }
      400:
        description: Invalid input
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Not a JSON"
    """
    try:
        request_data = request.get_json()
    except:
        return "Not a JSON", 400
    if 'name' not in request_data:
        return "Missing name", 400
    new_amenity = Amenity(**request_data)
    new_amenity.save()
    return jsonify(new_amenity.to_json()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an existing amenity.

    Request body should be a JSON object with fields to update.

    Parameters:
      - name: amenity_id
        in: path
        type: string
        description: The ID of the amenity to update.
        required: true
        example: "cf701d1a-3c19-4bac-bd99-15321f1140f2"

    Responses:
      200:
        description: The updated amenity
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Amenity'
            examples:
              value: {
                "__class__": "Amenity",
                "created_at": "2017-03-25T02:17:06",
                "id": "cf701d1a-3c19-4bac-bd99-15321f1140f2",
                "name": "Dog(s)",
                "updated_at": "2017-03-25T02:17:06"
              }
      400:
        description: Invalid input
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Not a JSON"
      404:
        description: Amenity not found
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Not found"
    """
    try:
        request_data = request.get_json()
    except:
        return "Not a JSON", 400
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    for field in ("id", "created_at", "updated_at"):
        request_data.pop(field, None)
    for key, value in request_data.items():
        setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_json()), 200
