from flask import Blueprint, request, jsonify
from src.Application.User.Services.UserApplicationService import UserApplicationService

auth_bp = Blueprint('auth', __name__)
user_app_service = UserApplicationService()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    user, response, status_code = user_app_service.register_user(data)

    if not user:
        return jsonify(response), status_code

    return jsonify(response), status_code
