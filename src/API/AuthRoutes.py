from flask import Blueprint, request, jsonify
from src.Application.User.Services.UserApplicationService import UserApplicationService
from src.Infrastructure.User.UserRepository import UserRepository
from src.Infrastructure.User.PasswordResetTokenRepository import PasswordResetTokenRepository
from src.Application.User.Services.PasswordResetTokenService import PasswordResetTokenService
from src.Application.User.Services.EncryptionService import EncryptionService

auth_bp = Blueprint('auth', __name__)
user_repository = UserRepository()
token_repository = PasswordResetTokenRepository()
password_reset_service = PasswordResetTokenService(token_repository)
user_app_service = UserApplicationService(user_repository, token_repository)
encryption_service = EncryptionService()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    user, response, status_code = user_app_service.register_user(data)

    if not user:
        return jsonify(response), status_code

    return jsonify(response), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user, response, status_code = user_app_service.login_user(data)

    if not user:
        return jsonify(response), status_code

    return jsonify(response), status_code

@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    
    # Request username, old_password, and new_password
    data = request.get_json()
    
    username = request.json.get('username')
    if not username:
        return jsonify({'error': 'User not authenticated'}), 401

    _, response, status_code = user_app_service.change_password(username, data)
    return jsonify(response), status_code

@auth_bp.route('/change-email', methods=['POST'])
def change_email():
    #Allows an authenticated user to change their email.
    #Requires: username, old_email, new_email, password

    # Get JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    username = data.get('username')
    if not username:
        return jsonify({'error': 'User not authenticated'}), 401

    # Call the application service to handle the email change logic
    _, response, status_code = user_app_service.change_email(username, data)

    return jsonify(response), status_code

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    # Delegate all logic to UserApplicationService
    data = request.get_json()
    user, response, status_code = user_app_service.request_password_reset(data)
    return jsonify(response), status_code

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    # Delegate all logic to UserApplicationService
    data = request.get_json()
    user, response, status_code = user_app_service.reset_password(data)
    return jsonify(response), status_code