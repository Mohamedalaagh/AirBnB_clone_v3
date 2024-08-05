#!/usr/bin/python3
"""
This module provides endpoints for managing user resources.
"""
from api.v1.views import (app_views, User, storage)
from flask import (abort, jsonify, request)

@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """
    Retrieves user information.

    - If `user_id` is not provided, returns a list of all users.
    - If `user_id` is provided, returns the details of the specified user.

    Parameters:
      - name: user_id
        in: path
        type: string
        description: The ID of the user to retrieve. If not provided, retrieves all users.
        required: false
        example: "32c11d3d-99a1-4406-ab41-7b6ccb7dd760"

    Responses:
      200:
        description: A list of users or a single user object
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
            examples:
              single:
                value: {
                  "__class__": "User",
                  "created_at": "2017-03-25T02:17:06",
                  "email": "noemail18@gmail.com",
                  "first_name": "Susan",
                  "id": "32c11d3d-99a1-4406-ab41-7b6ccb7dd760",
                  "last_name": "Finney",
                  "updated_at": "2017-03-25T02:17:06"
                }
              list:
                value: [
                  {
                    "__class__": "User",
                    "created_at": "2017-03-25T02:17:06",
                    "email": "noemail18@gmail.com",
                    "first_name": "Susan",
                    "id": "32c11d3d-99a1-4406-ab41-7b6ccb7dd760",
                    "last_name": "Finney",
                    "updated_at": "2017-03-25T02:17:06"
                  }
                ]
    """
    if user_id is None:
        users = [user.to_json() for user in storage.all("User").values()]
        return jsonify(users)
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a user by ID.

    Parameters:
      - name: user_id
        in: path
        type: string
        description: The ID of the user to delete.
        required: true
        example: "32c11d3d-99a1-4406-ab41-7b6ccb7dd760"

    Responses:
      200:
        description: Confirmation of successful deletion
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User deleted successfully"
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a new user.

    The request body must include `email` and `password`.

    Responses:
      201:
        description: The created user
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
            examples:
              value: {
                "__class__": "User",
                "created_at": "2017-03-25T02:17:06",
                "email": "noemail18@gmail.com",
                "first_name": "Susan",
                "id": "32c11d3d-99a1-4406-ab41-7b6ccb7dd760",
                "last_name": "Finney",
                "updated_at": "2017-03-25T02:17:06"
              }
      400:
        description: Invalid input or missing required fields
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Missing email" or "Missing password"
    """
    try:
        request_data = request.get_json()
    except:
        return "Not a JSON", 400
    if 'email' not in request_data:
        return "Missing email", 400
    if 'password' not in request_data:
        return "Missing password", 400
    new_user = User(**request_data)
    new_user.save()
    return jsonify(new_user.to_json()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates an existing user.

    The request body can include any fields to update except `id`, `email`, `created_at`, and `updated_at`.

    Parameters:
      - name: user_id
        in: path
        type: string
        description: The ID of the user to update.
        required: true
        example: "32c11d3d-99a1-4406-ab41-7b6ccb7dd760"

    Responses:
      200:
        description: The updated user
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
            examples:
              value: {
                "__class__": "User",
                "created_at": "2017-03-25T02:17:06",
                "email": "noemail18@gmail.com",
                "first_name": "Susan",
                "id": "32c11d3d-99a1-4406-ab41-7b6ccb7dd760",
                "last_name": "Finney",
                "updated_at": "2017-03-25T02:17:06"
              }
      400:
        description: Invalid input or not a JSON
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Not a JSON"
      404:
        description: User not found
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
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    for field in ("id", "email", "created_at", "updated_at"):
        request_data.pop(field, None)
    for key, value in request_data.items():
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_json()), 200

