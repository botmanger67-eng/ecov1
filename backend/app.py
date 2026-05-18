import os
from flask import Flask
from flask_cors import CORS
from backend.config import Config
from backend.models import db
from backend.routes import register_routes


def create_app(config_class=Config) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config_class: Configuration class (default: Config).

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    try:
        db.init_app(app)
    except Exception as e:
        app.logger.error(f"Failed to initialize database: {e}")
        raise

    # Enable CORS for frontend
    try:
        CORS(app, resources={r"/api/*": {"origins": "*"}})
    except Exception as e:
        app.logger.warning(f"CORS initialization failed: {e}")

    # Register all routes (blueprints or direct)
    try:
        register_routes(app)
    except Exception as e:
        app.logger.error(f"Failed to register routes: {e}")
        raise

    # Create database tables if they don't exist
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Failed to create database tables: {e}")
            raise

    return app


# Create the application instance
app = create_app()

if __name__ == "__main__":
    debug_mode = app.config.get("DEBUG", False)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)