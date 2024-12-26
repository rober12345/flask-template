# Flask imports
from flask import Blueprint, request, Response
from flask_limiter import ExemptionScope
from werkzeug.exceptions import HTTPException
from flask_limiter.errors import RateLimitExceeded
import logging

# Local imports
from app.extensions import limiter
from app.utils.api import error_response
from app.utils.cache import get_cached_response, set_cached_response

# Define the main API Blueprint
api_bp = Blueprint("api", __name__, url_prefix="/api")

# Exempt from rate limiting
limiter.exempt(
    api_bp,
    flags=ExemptionScope.DEFAULT
    | ExemptionScope.APPLICATION
    | ExemptionScope.DESCENDENTS,
)

# Error handler
@api_bp.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, RateLimitExceeded):
        current_limit = error.limit.limit
        return error_response(f"Too many requests: {current_limit}", 429)
    elif isinstance(error, HTTPException):
        return error_response(error.description, error.code)
    else:
        logging.error(error)
        return error_response("Internal Server Error", 500)


# Before request handler (Cache Lookup)
@api_bp.before_request
def before_request():
    cached_response = get_cached_response(request)
    if cached_response is not None:
        return cached_response


# After request handler (Cache Store)
@api_bp.after_request
def after_request(response: Response):
    if response.headers.get("Is-Cached-Response") == "1":
        response.headers.remove("Is-Cached-Response")
        set_cached_response(request, response)
    return response


# Import and register sub-blueprints
from .predictor import predictor_bp
from .data_ingestion import data_ingestion_bp
from .tests import tests_bp

api_bp.register_blueprint(predictor_bp, url_prefix='/predict')
api_bp.register_blueprint(data_ingestion_bp, url_prefix='/data')
api_bp.register_blueprint(tests_bp, url_prefix='/tests')
