"""Input validators for API requests."""


def validate_text_input(data):
    """Validate text input for analysis/translation endpoints.

    Args:
        data: Request JSON body.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if not data:
        return False, "Request body is required"

    text = data.get("text", "").strip()
    if not text:
        return False, "Text field is required and cannot be empty"

    if len(text) > 10000:
        return False, "Text exceeds maximum length of 10,000 characters"

    return True, None


def validate_script(script):
    """Validate transliteration script name.

    Args:
        script: Script name string.

    Returns:
        Tuple of (is_valid, normalized_script).
    """
    valid_scripts = {"devanagari", "iast", "hk", "slp1", "itrans"}
    script_lower = script.lower().strip() if script else "devanagari"

    if script_lower not in valid_scripts:
        return False, None

    return True, script_lower


def validate_image_file(file):
    """Validate uploaded image file.

    Args:
        file: FileStorage object from Flask request.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if not file or file.filename == "":
        return False, "No file selected"

    allowed_extensions = {"png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"}
    extension = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""

    if extension not in allowed_extensions:
        return False, f"File type '.{extension}' not allowed. Use: {', '.join(allowed_extensions)}"

    return True, None
