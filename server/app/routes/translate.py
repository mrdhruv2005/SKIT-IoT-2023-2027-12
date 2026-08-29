"""Translation routes — Sanskrit to Hindi/English with Padaccheda."""

from flask import Blueprint, request, jsonify

translate_bp = Blueprint("translate", __name__)


@translate_bp.route("/", methods=["POST"])
def translate():
    """
    Simple translation (Sanskrit → Hindi/English).

    Request body:
        {
            "text": "Sanskrit text",
            "target_language": "hindi" | "english",
        }
    """
    data = request.get_json()
    if not data or not data.get("text"):
        return jsonify({"error": "No text provided"}), 400

    # TODO: Implement in Phase 4A
    return jsonify({
        "message": "Translation endpoint — coming in Phase 4",
        "input_text": data.get("text"),
    }), 200


@translate_bp.route("/padaccheda", methods=["POST"])
def translate_padaccheda():
    """
    Detailed word-by-word analysis (Padaccheda mode).

    Request body:
        {
            "text": "Sanskrit text",
            "target_language": "hindi" | "english",
        }
    """
    data = request.get_json()
    if not data or not data.get("text"):
        return jsonify({"error": "No text provided"}), 400

    # TODO: Implement in Phase 4A
    return jsonify({
        "message": "Padaccheda endpoint — coming in Phase 4",
        "input_text": data.get("text"),
    }), 200


@translate_bp.route("/languages", methods=["GET"])
def list_languages():
    """List supported target languages."""
    return jsonify({
        "languages": [
            {"code": "hindi", "name": "Hindi", "native": "हिन्दी"},
            {"code": "english", "name": "English", "native": "English"},
        ]
    }), 200

# AI Translation Services Module
