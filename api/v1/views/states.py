#!/usr/bin/python3
"""
This module handles all routes for the State model.
Provides CRUD operations and other endpoints to interact with the State data.
"""
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import abort, jsonify, make_response, request

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def view_all_states():
    """
    Retrieves a list of all states.
    ---
    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The class name of the object
          created_at:
            type: string
            description: The creation date of the object
          id:
            type: string
            description: The ID of the state
          name:
            type: string
            description: The name of the state
          updated_at:
            type: string
            description: The last update date of the object

    responses:
      200:
        description: A list of dictionaries, each representing a State
        schema:
          $ref: '#/definitions/State'
        examples:
          [{'__class__': 'State', 'created_at': '2017-03-25T02:17:06',
            'id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f', 'name': 'Oregon',
            'updated_at': '2017-03-25T02:17:06'}]
    """
    all_states = [state.to_json() for state in storage.all("State").values()]
    return jsonify(all_states)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def view_one_state(state_id=None):
    """
    Retrieves a state by its ID.
    ---
    parameters:
      - name: state_id
        in: path
        type: string
        required: true
        description: The ID of the state

    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The class name of the object
          created_at:
            type: string
            description: The creation date of the object
          id:
            type: string
            description: The ID of the state
          name:
            type: string
            description: The name of the state
          updated_at:
            type: string
            description: The last update date of the object

    responses:
      200:
        description: A dictionary representing the desired State object
        schema:
          $ref: '#/definitions/State'
        examples:
          {'__class__': 'State', 'created_at': '2017-03-25T02:17:06',
           'id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f', 'name': 'Oregon',
           'updated_at': '2017-03-25T02:17:06'}
    """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_json())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """
    Deletes a state by its ID.
    ---
    parameters:
      - name: state_id
        in: path
        type: string
        required: true
        description: The ID of the state

    responses:
      200:
        description: An empty dictionary indicating successful deletion
        examples:
          {}
    """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a new State object based on the JSON body.
    ---
    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The class name of the object
          created_at:
            type: string
            description: The creation date of the object
          id:
            type: string
            description: The ID of the state
          name:
            type: string
            description: The name of the state
          updated_at:
            type: string
            description: The last update date of the object

    responses:
      201:
        description: A dictionary representing the newly created State
        schema:
          $ref: '#/definitions/State'
        examples:
          {'__class__': 'State', 'created_at': '2017-03-25T02:17:06',
           'id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f', 'name': 'Oregon',
           'updated_at': '2017-03-25T02:17:06'}
    """
    request_data = None
    try:
        request_data = request.get_json()
    except Exception:
        request_data = None
    if request_data is None:
        return "Not a JSON", 400
    if 'name' not in request_data:
        return "Missing name", 400
    new_state = State(**request_data)
    new_state.save()
    return jsonify(new_state.to_json()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """
    Updates a State object based on the JSON body.
    ---
    parameters:
      - name: state_id
        in: path
        type: string
        required: true
        description: The ID of the state

    definitions:
      State:
        type: object
        properties:
          __class__:
            type: string
            description: The class name of the object
          created_at:
            type: string
            description: The creation date of the object
          id:
            type: string
            description: The ID of the state
          name:
            type: string
            description: The name of the state
          updated_at:
            type: string
            description: The last update date of the object

    responses:
      200:
        description: A dictionary representing the updated State
        schema:
          $ref: '#/definitions/State'
        examples:
          {'__class__': 'State', 'created_at': '2017-03-25T02:17:06',
           'id': '10098698-bace-4bfb-8c0a-6bae0f7f5b8f', 'name': 'Oregon',
           'updated_at': '2017-03-25T02:17:06'}
    """
    try:
        request_data = request.get_json()
    except Exception:
        request_data = None
    if request_data is None:
        return "Not a JSON", 400
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    for key in ("id", "created_at", "updated_at"):
        request_data.pop(key, None)
    for key, value in request_data.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_json()), 200

