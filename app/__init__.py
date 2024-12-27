from flask import Flask
import os

# Import your extensions
from app.extensions import db, cors, csrf, cache, bcrypt, limiter, login_manager
from app.routes.api.predictor import predictor_bp
from app.routes.api.data_ingestion import data_ingestion_bp  # Import data ingestion blueprint

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
    app.register_blueprint(predictor_bp, url_prefix='/api/predict')  # Register predictor with prefix
    app.register_blueprint(data_ingestion_bp, url_prefix='/api/data')  # Register data ingestion
    # Register other blueprints as needed
    from app.routes import auth_bp, pages_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)

    # Print the URL map to see available routes
    print(app.url_map)

    # Global Rate Limit Checker
    app.before_request(lambda: limiter.check())

    return app
