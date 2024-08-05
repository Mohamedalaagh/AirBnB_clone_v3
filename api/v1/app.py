#!/usr/bin/python3
"""app.py to connect to API"""

import sys
import os
from flask import Flask, jsonify, make_response
from flask_cors import CORS

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from models import storage
from api.v1.views import app_views

# Create an instance of Flask
app = Flask(__name__)

# Register the blueprint app_views
app.register_blueprint(app_views)

# Enable CORS for the API
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def teardown_appcontext(exception):
    """Handle teardown of the app context"""
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors with a JSON response"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    # Get host and port from environment variables or default to 0.0.0.0 and 5000
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))

    # Run the Flask app with threading enabled
    app.run(host=host, port=port, threaded=True)
