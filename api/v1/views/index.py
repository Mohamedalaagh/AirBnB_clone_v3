#!/usr/bin/python3
"""
This module defines the routes for the status and statistics endpoints of the API.
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify

@app_views.route('/status/')
def get_status():
    """
    Endpoint that returns the current status of the API.
    
    Returns:
        Response: JSON response with the status of the API.
    
    ---
    definitions:
      Status:
        type: object
        properties:
          status:
            type: string
            example: "OK"
    
    responses:
      200:
        description: Dictionary with 'status' as key and 'OK' as value.
        schema:
          $ref: '#/definitions/Status'
        examples:
          application/json:
            {"status": "OK"}
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats/')
def get_stats():
    """
    Endpoint that returns the count of objects of each class.
    
    Returns:
        Response: JSON response with the count of each object type.
    
    ---
    definitions:
      Stats:
        type: object
        properties:
          amenities:
            type: integer
            example: 47
          cities:
            type: integer
            example: 36
          places:
            type: integer
            example: 154
          reviews:
            type: integer
            example: 718
          states:
            type: integer
            example: 27
          users:
            type: integer
            example: 31
    
    responses:
      200:
        description: Dictionary with the count of each object type.
        schema:
          $ref: '#/definitions/Stats'
        examples:
          application/json:
            {
              "amenities": 47,
              "cities": 36,
              "places": 154,
              "reviews": 718,
              "states": 27,
              "users": 31
            }
    """
    class_names = {
        "User": "users",
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states"
    }
    object_counts = {}
    for cls, endpoint in class_names.items():
        object_counts[endpoint] = storage.count(cls)
    return jsonify(object_counts)
