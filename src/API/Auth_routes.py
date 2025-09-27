from flask import Blueprint, request, jsonify
from src.Model.User.UserManager import UserManager
from src.Application.User.UserAuthent import UserAuthent

auth_bp = Blueprint('auth', __name__)
user_manager = UserManager()
user_authentication = UserAuthent()


def validate_request_data(data, required_fields):
    if not data:
        return False, (jsonify({'error': 'Invalid input'}), 400)

    for field in required_fields:
        if field not in data:
            return False, (jsonify({'error': f'Missing field: {field}'}), 400)

    return True, None


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['username', 'password', 'email']

    is_valid, error_response = validate_request_data(data, required_fields)
    if not is_valid:
        return error_response
    
    
    user, message = user_manager.create_user(
        username=data['username'],
        password=data['password'],
        email=data['email']
    )

    if not user:
        return jsonify({'error': message}), 400

    return jsonify({'message': message, 'user': user.to_dict()}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    required_fields = ['username', 'password']

    is_valid, error_response = validate_request_data(data, required_fields)
    if not is_valid:
        return error_response

    user = user_manager.get_user_by_username(data['username'])
    if not user or not user_authentication.verify_password(data['password'], user.password_hash):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    jwt_token = user_authentication.generate_token(user)
    print(jwt_token)
    #TODO @Paula: return token

    return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
