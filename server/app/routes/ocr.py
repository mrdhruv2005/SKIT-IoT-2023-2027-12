"""OCR routes — image upload and text extraction with meter-aware correction."""

from flask import Blueprint, request, jsonify

ocr_bp = Blueprint("ocr", __name__)


@ocr_bp.route("/extract", methods=["POST"])
def extract_text():
    """
    Upload an image and extract Sanskrit text via OCR.
    Optionally applies meter-aware correction.

    Request: multipart/form-data with 'image' file
    """
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files["image"]
    if image_file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # TODO: Implement in Phase 5
    return jsonify({
        "message": "OCR extraction endpoint — coming in Phase 5",
        "filename": image_file.filename,
    }), 200
