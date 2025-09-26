from flask import Blueprint, request, jsonify
from src.Model.User.UserManager import UserManager

auth_bp = Blueprint('auth', __name__)
user_manager = UserManager()


def validate_request_data(data, required_fields):
    if not data:
        return False, jsonify({'error': 'Invalid input'}), 400

    for field in required_fields:
        if field not in data:
            return False, jsonify, ({'error': f'Missing field: {field}'}), 400
    
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
