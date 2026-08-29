"""Chandas analysis routes — meter identification and syllable analysis.

Endpoints:
    POST /api/chandas/analyze    — Full verse analysis pipeline
    POST /api/chandas/syllabify  — Syllable breakdown only
    GET  /api/chandas/meters     — List all meters (pagination, search)
    GET  /api/chandas/meters/:id — Meter details + examples
"""

from flask import Blueprint, request, jsonify, current_app

from app.services.chandas_engine import (
    SyllableParser,
    LaghuGuruClassifier,
    GanaAnalyzer,
    MatraCounter,
    MeterDatabase,
    MeterMatcher,
)

chandas_bp = Blueprint("chandas", __name__)

# Lazy-initialized singletons
_parser = None
_classifier = None
_gana_analyzer = None
_matra_counter = None
_meter_db = None
_meter_matcher = None


def _get_engine():
    """Get or initialize the engine components (lazy singleton)."""
    global _parser, _classifier, _gana_analyzer, _matra_counter, _meter_db, _meter_matcher

    if _parser is None:
        _parser = SyllableParser()
        _classifier = LaghuGuruClassifier()
        _gana_analyzer = GanaAnalyzer()
        _matra_counter = MatraCounter()
        _meter_db = MeterDatabase(current_app.config.get("METER_DATA_DIR"))
        _meter_db.load()
        _meter_matcher = MeterMatcher(_meter_db)

    return _parser, _classifier, _gana_analyzer, _matra_counter, _meter_db, _meter_matcher


@chandas_bp.route("/analyze", methods=["POST"])
def analyze_verse():
    """
    Full verse analysis: syllable parsing, L-G classification,
    Gaṇa analysis, Mātrā count, and meter identification.

    Request body:
        {
            "text": "Sanskrit verse text",
            "script": "devanagari" | "iast" | "hk" | "slp1" | "auto",
            "enable_sandhi": false
        }

    Response:
        {
            "input_text": "...",
            "devanagari_text": "...",
            "script_detected": "devanagari",
            "padas": [...],
            "analysis": {
                "syllables": [...],
                "lg_patterns": [...],
                "gana_analysis": [...],
                "matra_counts": [...]
            },
            "meter": {
                "identified": true,
                "name": "...",
                "name_devanagari": "...",
                "category": "...",
                "tier_used": 1,
                "confidence": 1.0,
                "all_matches": [...]
            }
        }
    """
    data = request.get_json()
    if not data or not data.get("text"):
        return jsonify({"error": "No text provided"}), 400

    text = data["text"].strip()
    script = data.get("script", "auto")

    if len(text) > 10000:
        return jsonify({"error": "Text exceeds maximum length of 10,000 characters"}), 400

    try:
        parser, classifier, gana_analyzer, matra_counter, meter_db, meter_matcher = _get_engine()

        # Step 1: Parse into syllables
        parse_result = parser.parse(text, script)

        if not parse_result.padas:
            return jsonify({
                "error": "Could not parse any pādas from the input text. "
                         "Please check the input format.",
                "input_text": text,
            }), 400

        # Step 2: Classify L-G for each pāda
        lg_results = classifier.classify_verse(parse_result.syllables_by_pada)
        lg_patterns = [r.pattern for r in lg_results]

        # Step 3: Gaṇa analysis
        gana_results = gana_analyzer.analyze_verse(lg_patterns)

        # Step 4: Mātrā count
        matra_results = matra_counter.count_verse(lg_patterns)

        # Step 5: Meter identification
        match_result = meter_matcher.identify(lg_patterns, text)

        # Build response
        syllable_data = []
        for pada_idx, (syllables, lg_result) in enumerate(
            zip(parse_result.syllables_by_pada, lg_results)
        ):
            pada_syllables = []
            for cs in lg_result.classified_syllables:
                pada_syllables.append({
                    "text": cs.syllable.text,
                    "classification": cs.classification,
                    "reason": cs.reason,
                    "is_long_vowel": cs.syllable.is_long_vowel,
                    "has_anusvara": cs.syllable.has_anusvara,
                    "has_visarga": cs.syllable.has_visarga,
                    "is_pada_final": cs.syllable.is_pada_final,
                    "position": cs.syllable.position,
                })
            syllable_data.append(pada_syllables)

        gana_data = []
        for gr in gana_results:
            gana_data.append({
                "formula": gr.formula,
                "formula_devanagari": gr.formula_devanagari,
                "ganas": [
                    {
                        "pattern": g.pattern,
                        "name": g.name_iast,
                        "name_devanagari": g.name_devanagari,
                        "label": g.label,
                        "is_suffix": g.is_suffix,
                    }
                    for g in gr.ganas
                ],
            })

        matra_data = [
            {
                "matra_count": mr.matra_count,
                "per_syllable": mr.matra_per_syllable,
            }
            for mr in matra_results
        ]

        # Meter match data
        meter_data = {"identified": False}
        if match_result.best_match:
            bm = match_result.best_match
            meter_data = {
                "identified": True,
                "name": bm.meter.name_iast,
                "name_devanagari": bm.meter.name_devanagari,
                "name_english": bm.meter.name_english,
                "id": bm.meter.id,
                "category": bm.meter.category,
                "syllables_per_pada": bm.meter.syllables_per_pada,
                "pattern": bm.meter.pattern,
                "gana_formula": bm.meter.gana_formula,
                "description": bm.meter.description,
                "example_verse": bm.meter.example_verse,
                "example_source": bm.meter.example_source,
                "tier_used": bm.tier,
                "confidence": bm.confidence,
                "edit_distance": bm.edit_distance,
                "all_matches": [
                    {
                        "name": m.meter.name_iast,
                        "id": m.meter.id,
                        "tier": m.tier,
                        "confidence": m.confidence,
                        "edit_distance": m.edit_distance,
                    }
                    for m in match_result.matches[:5]
                ],
            }

        response = {
            "input_text": text,
            "devanagari_text": parse_result.devanagari_text,
            "script_detected": parse_result.script,
            "padas": parse_result.padas,
            "analysis": {
                "syllables": syllable_data,
                "lg_patterns": lg_patterns,
                "gana_analysis": gana_data,
                "matra_counts": matra_data,
            },
            "meter": meter_data,
        }

        return jsonify(response), 200

    except Exception as e:
        current_app.logger.error(f"Error analyzing verse: {e}", exc_info=True)
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


@chandas_bp.route("/syllabify", methods=["POST"])
def syllabify():
    """
    Syllable breakdown only (without meter identification).

    Request body:
        {"text": "Sanskrit text", "script": "devanagari"}

    Response:
        {
            "input_text": "...",
            "padas": [...],
            "syllables": [[{...}, ...], ...],
            "lg_patterns": [...],
            "total_syllables": 32
        }
    """
    data = request.get_json()
    if not data or not data.get("text"):
        return jsonify({"error": "No text provided"}), 400

    text = data["text"].strip()
    script = data.get("script", "auto")

    try:
        parser, classifier, _, _, _, _ = _get_engine()

        # Parse into syllables
        parse_result = parser.parse(text, script)

        # Classify L-G
        lg_results = classifier.classify_verse(parse_result.syllables_by_pada)

        # Build response
        syllable_data = []
        for lg_result in lg_results:
            pada_syllables = []
            for cs in lg_result.classified_syllables:
                pada_syllables.append({
                    "text": cs.syllable.text,
                    "classification": cs.classification,
                    "reason": cs.reason,
                    "is_long_vowel": cs.syllable.is_long_vowel,
                    "has_anusvara": cs.syllable.has_anusvara,
                    "has_visarga": cs.syllable.has_visarga,
                    "position": cs.syllable.position,
                })
            syllable_data.append(pada_syllables)

        return jsonify({
            "input_text": text,
            "devanagari_text": parse_result.devanagari_text,
            "script_detected": parse_result.script,
            "padas": parse_result.padas,
            "syllables": syllable_data,
            "lg_patterns": [r.pattern for r in lg_results],
            "total_syllables": parse_result.total_syllables,
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error syllabifying: {e}", exc_info=True)
        return jsonify({"error": f"Syllabification failed: {str(e)}"}), 500


@chandas_bp.route("/meters", methods=["GET"])
def list_meters():
    """
    List all meters with pagination and search.

    Query params:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 20, max: 100)
        search (str): Search query (name)
        category (str): Filter by category
    """
    try:
        _, _, _, _, meter_db, _ = _get_engine()

        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 20, type=int), 100)
        search = request.args.get("search", "").strip()
        category = request.args.get("category", "").strip()

        # Get meters
        if search:
            meters = meter_db.search(search)
        elif category:
            meters = meter_db.get_by_category(category)
        else:
            meters = meter_db.get_all_meters()

        # Paginate
        total = len(meters)
        start = (page - 1) * per_page
        end = start + per_page
        paginated = meters[start:end]

        return jsonify({
            "meters": [m.to_dict() for m in paginated],
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
            "categories": list(meter_db._by_category.keys()),
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error listing meters: {e}", exc_info=True)
        return jsonify({"error": f"Failed to list meters: {str(e)}"}), 500


@chandas_bp.route("/meters/<string:meter_id>", methods=["GET"])
def get_meter(meter_id):
    """Get details for a specific meter."""
    try:
        _, _, _, _, meter_db, _ = _get_engine()

        meter = meter_db.get_by_id(meter_id)
        if meter is None:
            return jsonify({"error": f"Meter '{meter_id}' not found"}), 404

        return jsonify({"meter": meter.to_dict()}), 200

    except Exception as e:
        current_app.logger.error(f"Error getting meter: {e}", exc_info=True)
        return jsonify({"error": f"Failed to get meter: {str(e)}"}), 500
