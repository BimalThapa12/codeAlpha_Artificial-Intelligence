"""
Translation Service
====================
Handles text translation using deep-translator (Google Translate backend).
Falls back gracefully with detailed error messages.
"""
from deep_translator import GoogleTranslator
from typing import Optional


# Complete language map: display name -> language code
LANGUAGES = {
    "Auto Detect": "auto",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Kinyarwanda": "rw",
    "Korean": "ko",
    "Kurdish": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Nyanja (Chichewa)": "ny",
    "Odia (Oriya)": "or",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tagalog (Filipino)": "tl",
    "Tajik": "tg",
    "Tamil": "ta",
    "Tatar": "tt",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Turkmen": "tk",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
}


def get_language_code(language_name: str) -> Optional[str]:
    """Convert a display language name to its ISO code."""
    return LANGUAGES.get(language_name)


def translate_text(text: str, source_lang: str, target_lang: str) -> dict:
    """
    Translate text from source_lang to target_lang.

    Args:
        text: The text to translate.
        source_lang: Source language code (e.g., 'en') or 'auto'.
        target_lang: Target language code (e.g., 'fr').

    Returns:
        dict with keys: success, translated_text, source_lang, target_lang, error
    """
    if not text or not text.strip():
        return {
            "success": False,
            "error": "Input text cannot be empty.",
            "translated_text": "",
        }

    if not target_lang:
        return {
            "success": False,
            "error": "Target language must be specified.",
            "translated_text": "",
        }

    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        translated = translator.translate(text.strip())

        return {
            "success": True,
            "translated_text": translated,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "error": None,
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Translation failed: {str(e)}",
            "translated_text": "",
        }


def get_all_languages() -> dict:
    """Return the full language dictionary."""
    return LANGUAGES
