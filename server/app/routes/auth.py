"""Authentication routes — register, login, refresh, profile."""

from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user.

    Request body:
        {"username": "...", "email": "...", "password": "..."}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required = ["username", "email", "password"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # TODO: Implement in Phase 6
    return jsonify({
        "message": "Registration endpoint — coming in Phase 6",
    }), 200


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Log in and receive JWT tokens.

    Request body:
        {"email": "...", "password": "..."}
    """
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password required"}), 400

    # TODO: Implement in Phase 6
    return jsonify({
        "message": "Login endpoint — coming in Phase 6",
    }), 200


@auth_bp.route("/profile", methods=["GET"])
def profile():
    """Get current user's profile (requires JWT)."""
    # TODO: Implement in Phase 6
    return jsonify({
        "message": "Profile endpoint — coming in Phase 6",
    }), 200
