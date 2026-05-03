"""
Text-to-Speech Service
========================
Converts text to audio using gTTS and saves it to the static/audio directory.
"""
import os
import uuid
import hashlib
from gtts import gTTS
from flask import current_app


def generate_speech(text: str, lang: str) -> dict:
    """
    Generate an audio file for the given text and language.

    Args:
        text: Text to convert to speech.
        lang: BCP-47 language code (e.g., 'en', 'fr', 'hi').

    Returns:
        dict with keys: success, audio_url, error
    """
    if not text or not text.strip():
        return {"success": False, "error": "Text cannot be empty.", "audio_url": ""}

    # Use a hash of text+lang as filename to avoid regenerating duplicates
    content_hash = hashlib.md5(f"{text}{lang}".encode()).hexdigest()
    filename = f"{content_hash}.mp3"

    audio_dir = current_app.config.get(
        "AUDIO_DIR",
        os.path.join(current_app.static_folder, "audio")
    )
    os.makedirs(audio_dir, exist_ok=True)
    filepath = os.path.join(audio_dir, filename)

    try:
        if not os.path.exists(filepath):
            tts = gTTS(text=text.strip(), lang=lang, slow=False)
            tts.save(filepath)

        # Return the URL path (served via Flask's static file handler)
        audio_url = f"/static/audio/{filename}"
        return {"success": True, "audio_url": audio_url, "error": None}

    except Exception as e:
        return {"success": False, "error": f"TTS failed: {str(e)}", "audio_url": ""}


def cleanup_old_audio(max_files: int = 50) -> None:
    """
    Keep audio directory from growing unbounded by removing oldest files
    when count exceeds max_files.
    """
    audio_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "static", "audio"
    )
    if not os.path.exists(audio_dir):
        return

    files = sorted(
        [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(".mp3")],
        key=os.path.getmtime
    )

    while len(files) > max_files:
        os.remove(files.pop(0))
