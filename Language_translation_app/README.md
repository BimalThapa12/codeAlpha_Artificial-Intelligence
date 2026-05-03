# Language Translation App — LinguaAI

A beautiful, full-featured **Language Translation Web App** built with **Python + Flask**, powered by **Google Translate** (via `deep-translator`), with **Text-to-Speech** and a **Copy to Clipboard** feature.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🌐 **100+ Languages** | Full Google Translate language support |
| 🔄 **Auto-detect** | Automatically detects the source language |
| 🔊 **Text-to-Speech** | Listen to both source and translated text |
| 📋 **Copy Button** | One-click copy the translation |
| ⌨️ **Keyboard Shortcut** | `Ctrl + Enter` to translate instantly |
| 🔀 **Swap Languages** | Swap source ↔ target languages in one click |
| ⚡ **Auto-translate** | Auto-translates 2 seconds after you stop typing |
| 🚀 **Quick Chips** | One-click language shortcuts (Spanish, French, Japanese…) |
| 📱 **Responsive** | Works on desktop, tablet, and mobile |

---

## 🗂️ Project Structure

```
Language_translation_app/
│
├── run.py                    # App entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
├── .gitignore
│
├── app/                      # Flask application package
│   ├── __init__.py           # App factory (create_app)
│   ├── config.py             # Configuration (env vars)
│   ├── routes.py             # URL routes + API endpoints
│   ├── translator.py         # Translation service (deep-translator)
│   └── tts_service.py        # Text-to-Speech service (gTTS)
│
├── templates/
│   └── index.html            # Main UI template (Jinja2)
│
└── static/
    ├── css/
    │   └── style.css         # Dark glassmorphism stylesheet
    ├── js/
    │   └── app.js            # Frontend JavaScript controller
    └── audio/                # Generated TTS audio files (auto-created)
```

---

## 🚀 Getting Started

### 1. Clone / Navigate to the project
```bash
cd Language_translation_app
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env if needed (optional — app works without any API keys)
```

### 5. Run the app
```bash
python run.py
```

### 6. Open in browser
Visit **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Main translation UI |
| `POST` | `/api/translate` | Translate text |
| `POST` | `/api/tts` | Text-to-speech audio |
| `GET` | `/api/languages` | Get all supported languages |

### `POST /api/translate`
```json
// Request
{ "text": "Hello world", "source_lang": "auto", "target_lang": "fr" }

// Response
{ "success": true, "translated_text": "Bonjour le monde", "source_lang": "auto", "target_lang": "fr" }
```

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, Flask 3, Flask-CORS
- **Translation**: `deep-translator` (Google Translate backend, no API key required)
- **TTS**: `gTTS` (Google Text-to-Speech)
- **Frontend**: Vanilla HTML5 + CSS3 + JavaScript (ES2022)
- **Design**: Dark glassmorphism, Inter font, animated gradients

---

## 📝 License
MIT — Free for personal and educational use.

> **CodeAlpha Internship Project**
