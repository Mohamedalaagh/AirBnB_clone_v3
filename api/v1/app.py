#!/usr/bin/python3
"""
This module sets up the Flask application for the AirBnB clone API.
"""

from api.v1.views import app_views
from flasgger import Swagger
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from os import getenv

# Initialize Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for the entire app
CORS(app, origins="0.0.0.0")

# Register the blueprint for the API views
app.register_blueprint(app_views)

# Initialize Swagger for API documentation
Swagger(app)

@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 errors (Not Found).
    
    Returns a JSON response with a 404 status code and an error message.
    
    Args:
        error: The error causing the handler to be invoked.

    Returns:
        Response: A JSON response with the error message.
    """
    return make_response(jsonify({"error": "Not found"}), 404)

@app.teardown_appcontext
def teardown(exception):
    """
    Handler for the app context teardown.
    
    This function is called whenever the app context is torn down. 
    It ensures that the storage session is closed.
    
    Args:
        exception: The exception that caused the teardown, if any.
    """
    storage.close()

if __name__ == "__main__":
    # Get the host and port from environment variables, with default values
    api_host = getenv("HBNB_API_HOST", "0.0.0.0")
    api_port = getenv("HBNB_API_PORT", "5000")

    # Run the Flask app
    app.run(host=api_host, port=api_port)
