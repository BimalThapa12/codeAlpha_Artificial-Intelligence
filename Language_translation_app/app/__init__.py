"""
App Package Initializer
=======================
Creates and configures the Flask application factory.
"""
from flask import Flask
from flask_cors import CORS
from .config import Config


def create_app(config_class=Config):
    """Application factory pattern."""
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )
    app.config.from_object(config_class)

    # Enable CORS for all routes
    CORS(app)

    # Register blueprints
    from .routes import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
