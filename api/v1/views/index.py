#!/usr/bin/python3
"""index.py to define API routes for status and statistics"""

from flask import Flask, Blueprint, jsonify
from models import storage
# Define the mapping of endpoint names to model names
hbnbText = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}

# Create a Blueprint instance for app_views
app_views = Blueprint('app_views', __name__)

@app_views.route('/status', strict_slashes=False)
def hbnb_status():
    """Returns the status of the API"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def hbnb_stats():
    """Returns statistics of the number of objects for each model"""
    return_dict = {}
    for key, value in hbnbText.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)

# Ensure this file is run directly and not imported
if __name__ == "__main__":
    # This script is intended to be used with the main application
    pass
