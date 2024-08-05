#!/usr/bin/python3
"""
API routes for handling Review objects.
"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves a list of all Review objects for a specified place.

    Args:
        place_id (str): The ID of the Place.

    Returns:
        A JSON list of dictionaries representing Review objects.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object by its ID.

    Args:
        review_id (str): The ID of the Review.

    Returns:
        A JSON dictionary representing the Review object.
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object by its ID.

    Args:
        review_id (str): The ID of the Review.

    Returns:
        An empty JSON dictionary with status code 200.
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review object for a specified place.

    Args:
        place_id (str): The ID of the Place.

    Returns:
        A JSON dictionary representing the new Review object with status code 201.
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    
    review_data = request.get_json()
    if 'user_id' not in review_data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    
    user = storage.get("User", review_data['user_id'])
    if user is None:
        abort(404)
    
    if 'text' not in review_data:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    
    review_data['place_id'] = place_id
    new_review = Review(**review_data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates an existing Review object by its ID.

    Args:
        review_id (str): The ID of the Review.

    Returns:
        A JSON dictionary representing the updated Review object.
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    
    for attribute, value in request.get_json().items():
        if attribute not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, attribute, value)
    
    review.save()
    return jsonify(review.to_dict())
