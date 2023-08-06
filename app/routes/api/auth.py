# Flask modules
from flask import Blueprint, request
from werkzeug.security import generate_password_hash, check_password_hash

# Other modules
import logging
from email_validator import validate_email, EmailNotValidError

# Local modules
from app.extensions import db
from app.models.user import User
from app.utils.auth import encode_token
from app.utils.api import success_response, error_response

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=['POST'])
def login():
    user_data = request.get_json()
    email = user_data.get("email")
    password = user_data.get("password")

    if not email:
        return error_response("Email address is required", 400)
    elif not password:
        return error_response("Password is required", 400)

    try:
        validated_email = validate_email(email)
    except EmailNotValidError:
        return error_response("Invalid email address", 400)

    clean_email = validated_email.normalized.lower()

    user = User.query.filter_by(email=clean_email).first()
    if not user:
        return error_response("User does not exist", 404)

    if not check_password_hash(user.password, password):
        return error_response("Invalid credentials", 404)

    auth_token = encode_token(user.id)
    result = {
        "message": "Successfully logged in",
        'auth_token': auth_token
    }
    return success_response(result, 200)


@auth_bp.route("/register", methods=['POST'])
def register():
    user_data = request.get_json()
    email = user_data.get("email")
    password = user_data.get("password")

    if not email:
        return error_response("Email address is required", 400)
    elif not password:
        return error_response("Password is required", 400)

    try:
        validated_email = validate_email(email)
    except EmailNotValidError:
        return error_response("Invalid email address", 400)

    clean_email = validated_email.normalized.lower()
    name = validated_email.local_part.lower()[:80]

    user = User.query.filter_by(email=clean_email).first()
    if user:
        return error_response("User already exists", 202)

    try:
        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        return success_response("User successfully registered", 201)

    except Exception as e:
        logging.error(e)
        return error_response("Error occurred, user registration failed", 401)


@auth_bp.route("/logout")
def logout():
    pass
