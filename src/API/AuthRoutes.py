from flask import Blueprint, request, jsonify, make_response, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
import jwt
import os
from src.Application.User.Services.UserApplicationService import UserApplicationService
from src.Application.User.Services.EncryptionService import EncryptionService
from src.Application.User.Services.ValidationService import ValidationService
from src.Application.User.Services.TokenService import TokenService
from src.Infrastructure.User.UserRepository import UserRepository
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository
from src.Application.Profiles.Services.ProfileApplicationService import (
    ProfileApplicationService,
)
from src.Application.User.Services.AccountApplicationService import (
    AccountApplicationService,
)
from src.Application.User.Services.AuthorizationService import AuthorizationService
from src.Model.Profiles.Roles import Role

auth_bp = Blueprint("auth", __name__)

user_repository = UserRepository()
validation_service = ValidationService()
encryption_service = EncryptionService()
token_service = TokenService()
profile_service = ProfileApplicationService(profile_repository=ProfileRepository())

account_app_service = AccountApplicationService(
    user_repository=user_repository,
    profile_service=profile_service,
    token_service=token_service,
)

user_app_service = UserApplicationService(
    user_repository=user_repository,
    validation_service=validation_service,
    encryption_service=encryption_service,
    token_service=token_service,
    profile_service=profile_service,
)
auth_service = AuthorizationService(user_app_service, profile_service)

# Configuración para Google OAuth
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_to="google.login_google_callback",
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
    ],
)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    user, response, status_code = user_app_service.register_user(data)

    if not user:
        return jsonify(response), status_code

    return jsonify(response), status_code


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user, response, token, status_code = user_app_service.login_user(data)

    if not user:
        return jsonify(response), status_code

    response_with_header = make_response(jsonify(response), status_code)
    response_with_header.headers["Authorization"] = f"Bearer {token}"

    return response_with_header


@google_bp.route("/login-google", methods=["GET"])
def login_google():
    return redirect(url_for("google.login"))


# User will be redirected here after login
@google_bp.route("/login-google/callback", methods=["GET"])
def login_google_callback():

    if not google.authorized:
        return jsonify({"error:" "User not authenticated"}), 401

    resp = google.get("https://www.googleapis.com/oauth2/v3/userinfo")

    if not resp.ok:
        return jsonify({"error:" "Couldn't get information from Google"}), 401

    user_info = resp.json()

    if "email" not in user_info:
        return jsonify({"error": "Couldn't get information from Google"}), 401

    user, response, status_code = user_app_service.login_with_google(user_info["email"])

    if not user:
        return jsonify(response), status_code

    response_with_token = make_response(jsonify(response), status_code)

    return response_with_token


@auth_bp.route("/change-password", methods=["POST"])
def change_password():
    is_auth, response, status_code = auth_service.is_authorized(
        request.headers,
        [Role.ADMIN, Role.GOD],
    )

    if not is_auth:
        return jsonify(response), status_code
    
    if "Authorization" not in request.headers or not request.headers["Authorization"]:
        return jsonify({"error": "Missing token"}), 401

    # Request username, old_password, and new_password
    data = request.get_json()

    username = request.json.get("username")
    if not username:
        return jsonify({"error": "User not authenticated"}), 401

    header = request.headers
    user, response, status_code = user_app_service.verify_valid_session(
        header, username
    )

    if not user:
        return jsonify(response), status_code

    _, response, status_code = user_app_service.change_password(user, data)
    return jsonify(response), status_code


@auth_bp.route("/regenerate-key", methods=["POST"])
def regenerate_key():
    is_auth, response, status_code = auth_service.is_authorized(
        request.headers,
        [Role.ADMIN, Role.GOD],
    )

    if not is_auth:
        return jsonify(response), status_code
    
    auth = request.headers.get("Authorization", "")
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return jsonify({"error": "Missing token"}), 401
    token = parts[1].strip()

    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        username = payload.get("username")
        if not username:
            return jsonify({"error": "Invalid token payload"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    user, resp, status = user_app_service.verify_valid_session(
        request.headers, username
    )
    if not user:
        return jsonify(resp), status

    _, resp, status = user_app_service.regenerate_key(user.username)
    return jsonify(resp), status


@auth_bp.route("/delete-account", methods=["DELETE"])
def delete_account():
    is_auth, response, status_code = auth_service.is_authorized(
        request.headers,
        [Role.ADMIN, Role.GOD],
    )

    if not is_auth:
        return jsonify(response), status_code
    
    is_auth = auth_service.is_superior_user(request)
    
    if not is_auth:
        return jsonify({"error": "The user has no permission to delete specified target"}), 403
    
    # Get username to delete from request body
    json_data = request.get_json()
    username_to_delete = json_data.get("username") if json_data else None

    if not username_to_delete:
        return jsonify({"error": "Username to delete is required"}), 400

    # Call the service to delete the user account
    user, response, status_code = account_app_service.delete_user_account(
        request.headers, username_to_delete
    )

    return jsonify(response), status_code
