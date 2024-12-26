from flask import Flask
import os

# Import your extensions
from app.extensions import db, cors, csrf, cache, bcrypt, limiter, login_manager

def create_app(debug: bool = False):
    # Check if debug environment variable was passed
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)
    debug = FLASK_DEBUG if FLASK_DEBUG else debug

    # Create the Flask application instance
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/",
    )

    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ManzanaOrganico1@localhost:5432/economic_data-db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app)
    csrf.init_app(app)
    cache.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    login_manager.init_app(app)

    # Import all models and create database tables
    with app.app_context():
        from app import models  # Adjust to your model import
        db.create_all()

        # Start scheduler if necessary
        from app.utils.scheduler import start_scheduler
        start_scheduler()

    # Register blueprints
    from app.routes import api_bp, pages_bp, auth_bp
    app.register_blueprint(api_bp, url_prefix='/api')  # Ensure api_bp corresponds to your routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)

    # Global Rate Limit Checker
    app.before_request(lambda: limiter.check())

    return app
