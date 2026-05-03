"""
Configuration Module
=====================
Loads environment variables and sets Flask configuration values.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-prod")
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5000))

    # Optional Google Cloud Translation API key
    # Leave empty to use the free deep-translator library
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

    # Audio output directory
    AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "audio")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"
