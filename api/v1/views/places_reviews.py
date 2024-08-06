#!/usr/bin/python3
"""
Review model routes for handling review-related endpoints.
"""
from flask import (abort, jsonify, request)
from api.v1.views import app_views
from models.review import Review
from models import storage

@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_reviews_for_place(place_id):
    """Retrieve all reviews for a specific place."""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    reviews = [review.to_json() for review in place.reviews]
    return jsonify(reviews)

@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """Retrieve a single review by its ID."""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_json())

@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """Delete a review by its ID."""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    storage.delete(review)
    return jsonify({}), 200

@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_review_for_place(place_id):
    """Create a new review for a specific place."""
    review_data = request.get_json()
    if not review_data:
        return "Not a JSON", 400
    if "user_id" not in review_data:
        return "Missing user_id", 400
    if "text" not in review_data:
        return "Missing text", 400

    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    
    user = storage.get("User", review_data["user_id"])
    if not user:
        abort(404)

    new_review = Review(**review_data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_json()), 201

@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Update an existing review by its ID."""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    update_data = request.get_json()
    if not update_data:
        return "Not a JSON", 400

    for key in ("id", "user_id", "place_id", "created_at", "updated_at"):
        update_data.pop(key, None)

    for key, value in update_data.items():
        setattr(review, key, value)
    
    review.save()
    return jsonify(review.to_json()), 200

