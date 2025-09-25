from flask import Blueprint, request, jsonify
from src.Model.User.UserManager import UserManager

auth_bp = Blueprint('auth', __name__)
user_manager = UserManager()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    
    required_fields = ['username', 'password', 'email']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
        
    user, message = user_manager.create_user(
        username=data['username'],
        password=data['password'],
        email=data['email']
    )

    if not user:
        return jsonify({'error': message}), 400
