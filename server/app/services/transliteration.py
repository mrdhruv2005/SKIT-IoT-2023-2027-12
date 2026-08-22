"""
Script conversion utility — thin wrapper around `indic-transliteration` library.

Supports: Devanagari, IAST, Harvard-Kyoto (HK), SLP1, ITRANS.
Used by the Chandas engine to normalize input before syllable parsing.
"""

import re
from indic_transliteration import sanscript, detect


# Mapping from our script names to indic_transliteration constants
SCRIPT_MAP = {
    "devanagari": sanscript.DEVANAGARI,
    "iast": sanscript.IAST,
    "hk": sanscript.HK,
    "slp1": sanscript.SLP1,
    "itrans": sanscript.ITRANS,
}

# Reverse mapping for detection results
DETECT_REVERSE_MAP = {
    sanscript.DEVANAGARI: "devanagari",
    sanscript.IAST: "iast",
    sanscript.HK: "hk",
    sanscript.SLP1: "slp1",
    sanscript.ITRANS: "itrans",
}


def to_devanagari(text, source_script="iast"):
    """Convert text from any supported script to Devanagari.

    Args:
        text: Input Sanskrit text.
        source_script: Source script name (e.g., 'iast', 'hk', 'slp1', 'itrans').

    Returns:
        Text in Devanagari script.

    Raises:
        ValueError: If the source script is not supported.
    """
    if not text or not text.strip():
        return ""

    source = SCRIPT_MAP.get(source_script.lower())
    if source is None:
        raise ValueError(
            f"Unsupported script: '{source_script}'. "
            f"Supported: {', '.join(SCRIPT_MAP.keys())}"
        )

    if source == sanscript.DEVANAGARI:
        return text  # Already Devanagari

    return sanscript.transliterate(text, source, sanscript.DEVANAGARI)


def to_iast(text, source_script="devanagari"):
    """Convert text from any supported script to IAST.

    Args:
        text: Input Sanskrit text.
        source_script: Source script name.

    Returns:
        Text in IAST (International Alphabet of Sanskrit Transliteration).

    Raises:
        ValueError: If the source script is not supported.
    """
    if not text or not text.strip():
        return ""

    source = SCRIPT_MAP.get(source_script.lower())
    if source is None:
        raise ValueError(
            f"Unsupported script: '{source_script}'. "
            f"Supported: {', '.join(SCRIPT_MAP.keys())}"
        )

    if source == sanscript.IAST:
        return text  # Already IAST

    return sanscript.transliterate(text, source, sanscript.IAST)


def transliterate(text, source_script, target_script):
    """Convert text between any two supported scripts.

    Args:
        text: Input text.
        source_script: Source script name.
        target_script: Target script name.

    Returns:
        Transliterated text.

    Raises:
        ValueError: If either script is not supported.
    """
    if not text or not text.strip():
        return ""

    source = SCRIPT_MAP.get(source_script.lower())
    target = SCRIPT_MAP.get(target_script.lower())

    if source is None:
        raise ValueError(f"Unsupported source script: '{source_script}'")
    if target is None:
        raise ValueError(f"Unsupported target script: '{target_script}'")

    if source == target:
        return text

    return sanscript.transliterate(text, source, target)


def detect_script(text):
    """Auto-detect the script of the input text.

    Uses heuristics based on Unicode code point ranges:
    - Devanagari: U+0900–U+097F
    - IAST: Latin characters with diacritics (ā, ī, ū, ṛ, ṝ, ṃ, ḥ, ṅ, ñ, ṭ, ḍ, ṇ, ś, ṣ)
    - Plain ASCII: Could be HK, SLP1, or ITRANS — defaults to IAST

    Args:
        text: Input text to detect.

    Returns:
        Detected script name string (e.g., 'devanagari', 'iast').
    """
    if not text or not text.strip():
        return "devanagari"

    text = text.strip()

    # Check for Devanagari Unicode range (U+0900 – U+097F)
    devanagari_count = sum(1 for ch in text if "\u0900" <= ch <= "\u097F")
    total_alpha = sum(1 for ch in text if ch.isalpha() or "\u0900" <= ch <= "\u097F")

    if total_alpha == 0:
        return "devanagari"

    if devanagari_count / total_alpha > 0.5:
        return "devanagari"

    # Check for IAST diacritical marks
    iast_diacritics = set("āīūṛṝṃḥṅñṭḍṇśṣĀĪŪṚṜṂḤṄÑṬḌṆŚṢ")
    if any(ch in iast_diacritics for ch in text):
        return "iast"

    # Check for SLP1-specific characters (uppercase in unusual positions)
    # SLP1 uses characters like 'S' for 'ś', 'z' for 'ṣ', 'f' for 'ṛ' etc.
    slp1_indicators = set("fFxXqQwWYR")
    if any(ch in slp1_indicators for ch in text):
        return "slp1"

    # Default to IAST for plain ASCII (could also be HK)
    return "iast"


def normalize(text, script="devanagari"):
    """Clean and normalize input text.

    Performs:
    - Strip leading/trailing whitespace
    - Normalize Unicode (NFC form)
    - Remove zero-width characters
    - Collapse multiple spaces

    Args:
        text: Input text.
        script: Script of the input (for script-specific normalization).

    Returns:
        Normalized text string.
    """
    import unicodedata

    if not text:
        return ""

    # Unicode NFC normalization
    text = unicodedata.normalize("NFC", text)

    # Remove zero-width characters (ZWJ, ZWNJ, etc.)
    text = re.sub(r"[\u200B-\u200F\u202A-\u202E\uFEFF]", "", text)

    # Collapse multiple whitespace into single space
    text = re.sub(r"\s+", " ", text)

    # Strip
    text = text.strip()

    return text
