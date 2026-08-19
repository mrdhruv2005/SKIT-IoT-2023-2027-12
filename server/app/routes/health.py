"""Health check route — used by UptimeRobot and for verifying the server is running."""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/api/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Chandas API",
        "version": "0.1.0",
    }), 200


@health_bp.route("/", methods=["GET"])
def root():
    """Root endpoint."""
    return jsonify({
        "message": "Chandas Identification & Sanskrit Translator API",
        "docs": "/api/health",
        "version": "0.1.0",
    }), 200
