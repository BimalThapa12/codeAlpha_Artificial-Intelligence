"""
Language Translation App - Flask Backend
=========================================
Entry point for the translation application.
"""
from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(
        host=app.config.get("HOST", "127.0.0.1"),
        port=int(app.config.get("PORT", 5000)),
        debug=app.config.get("FLASK_DEBUG", True)
    )
