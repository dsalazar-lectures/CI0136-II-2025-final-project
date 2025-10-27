from flask import Blueprint, request, jsonify
from src.Application.User.Services.UserApplicationService import UserApplicationService
from src.Application.User.Services.EncryptionService import EncryptionService
from src.Application.User.Services.ValidationService import ValidationService
from src.Application.User.Services.TokenService import TokenService
from src.Infrastructure.User.UserRepository import UserRepository
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository
from src.Application.Profiles.Services.ProfileApplicationService import (
    ProfileApplicationService,
)

auth_bp = Blueprint("auth", __name__)

user_repository = UserRepository()
validation_service = ValidationService()
encryption_service = EncryptionService()
token_service = TokenService()
profile_service = ProfileApplicationService(profile_repository=ProfileRepository())

user_app_service = UserApplicationService(
    user_repository=user_repository,
    validation_service=validation_service,
    encryption_service=encryption_service,
    token_service=token_service,
    profile_service=profile_service,
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

    user, response, status_code = user_app_service.login_user(data)

    if not user:
        return jsonify(response), status_code

    return jsonify(response), status_code
