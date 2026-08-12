"""History routes — user analysis history management."""

from flask import Blueprint, jsonify

history_bp = Blueprint("history", __name__)


@history_bp.route("/", methods=["GET"])
def list_history():
    """
    List user's analysis history (paginated).

    Query params: page, per_page, type (chandas/translation/ocr)
    """
    # TODO: Implement in Phase 6
    return jsonify({
        "message": "History listing endpoint — coming in Phase 6",
        "history": [],
    }), 200


@history_bp.route("/<int:history_id>", methods=["GET"])
def get_history_item(history_id):
    """Get a specific history item."""
    # TODO: Implement in Phase 6
    return jsonify({
        "message": f"History item {history_id} — coming in Phase 6",
    }), 200


@history_bp.route("/<int:history_id>", methods=["DELETE"])
def delete_history_item(history_id):
    """Delete a specific history item."""
    # TODO: Implement in Phase 6
    return jsonify({
        "message": f"Delete history item {history_id} — coming in Phase 6",
    }), 200
