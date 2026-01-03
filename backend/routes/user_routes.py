from flask import Blueprint, jsonify, request, session
from models.user import User
from extensions import db

# Keeping your prefix, but ensuring the frontend JS matches this path
user_bp = Blueprint("user", __name__, url_prefix="/api/user")

@user_bp.route("/me", methods=["GET"])
def get_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "name": user.name,
        "email": user.email,
        "bio": getattr(user, 'bio', "No bio available") # Added bio for the profile page
    })


@user_bp.route("/me", methods=["PUT", "POST"]) # Added POST to support various frontend fetch styles
def update_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.json
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Update fields based on the new Profile Page inputs
    user.name = data.get("name", user.name)
    
    # Check if your User model has a bio column; if so, update it
    if hasattr(user, 'bio'):
        user.bio = data.get("bio", user.bio)
        
    db.session.commit()

    return jsonify({
        "message": "Profile updated",
        "name": user.name,
        "bio": getattr(user, 'bio', "")
    })


@user_bp.route("/delete", methods=["DELETE"])
def delete_account():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
        
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        session.clear()
        return jsonify({"message": "Account deleted"})
    
    return jsonify({"error": "User not found"}), 404