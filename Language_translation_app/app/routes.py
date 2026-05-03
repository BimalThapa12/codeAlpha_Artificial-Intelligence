"""
Routes Module
==============
Defines the main UI route and REST API endpoints.
"""
from flask import Blueprint, render_template, request, jsonify
from .translator import translate_text, get_all_languages
from .tts_service import generate_speech

# Blueprint for HTML views
main_bp = Blueprint("main", __name__)

# Blueprint for JSON API endpoints
api_bp = Blueprint("api", __name__)


# ─────────────────────────────────────────────
# HTML Page Routes
# ─────────────────────────────────────────────

@main_bp.route("/")
def index():
    """Render the main translation interface."""
    languages = get_all_languages()
    return render_template("index.html", languages=languages)


# ─────────────────────────────────────────────
# API Routes
# ─────────────────────────────────────────────

@api_bp.route("/translate", methods=["POST"])
def translate():
    """
    Translate text between languages.

    Request JSON body:
        text        (str): Text to translate.
        source_lang (str): Source language code (e.g., 'en') or 'auto'.
        target_lang (str): Target language code (e.g., 'fr').

    Response JSON:
        success         (bool)
        translated_text (str)
        source_lang     (str)
        target_lang     (str)
        error           (str|null)
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON body."}), 400

    text = data.get("text", "").strip()
    source_lang = data.get("source_lang", "auto")
    target_lang = data.get("target_lang", "en")

    result = translate_text(text, source_lang, target_lang)
    status_code = 200 if result["success"] else 422
    return jsonify(result), status_code


@api_bp.route("/tts", methods=["POST"])
def text_to_speech():
    """
    Generate audio for given text.

    Request JSON body:
        text (str): Text to speak.
        lang (str): Language code for speech synthesis.

    Response JSON:
        success   (bool)
        audio_url (str)  — relative URL to the generated mp3 file
        error     (str|null)
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "error": "Invalid JSON body."}), 400

    text = data.get("text", "").strip()
    lang = data.get("lang", "en")

    result = generate_speech(text, lang)
    status_code = 200 if result["success"] else 422
    return jsonify(result), status_code


@api_bp.route("/languages", methods=["GET"])
def languages():
    """Return the full map of supported languages."""
    return jsonify({"success": True, "languages": get_all_languages()})
