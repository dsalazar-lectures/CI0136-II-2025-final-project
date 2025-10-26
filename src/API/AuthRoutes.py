from flask import Blueprint, request, jsonify
from src.Application.User.Services.UserApplicationService import UserApplicationService
from src.Infrastructure.User.UserRepository import UserRepository

auth_bp = Blueprint('auth', __name__)
user_repository = UserRepository()
user_app_service = UserApplicationService(user_repository)


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
