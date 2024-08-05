#!/usr/bin/python3
"""states.py"""

import sys
import os
from flask import abort, jsonify, make_response, request

# Add the path to the 'models' directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from models import storage
from models.state import State
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve information for all states."""
    states = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states)

@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieve information for a specified state."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404, description=f"State with id {state_id} not found")
    return jsonify(state.to_dict())

@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a state based on its state_id."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404, description=f"State with id {state_id} not found")
    state.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Create a new state."""
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    
    data = request.get_json()
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Update an existing state."""
    state = storage.get("State", state_id)
    if state is None:
        abort(404, description=f"State with id {state_id} not found")
    
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    
    data = request.get_json()
    for attr, val in data.items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    
    state.save()
    return jsonify(state.to_dict())
