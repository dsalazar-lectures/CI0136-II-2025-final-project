from src.Application.DTOs.UserDTO import UserDTO
from src.Database.User.UserRepository import UserRepository
from src.Application.Services.ValidationService import ValidationService


class UserApplicationService:
    def __init__(self):
        self.validation_service = ValidationService()
        self.user_repository = UserRepository()

    def validate_userdata(self, username, password, email):
        if not username or not isinstance(username, str):
            return False, "Username is required"
        if not password or not isinstance(password, str):
            return False, "Password is required"
        if not email or not isinstance(email, str):
            return False, "Email is required"
        if "@" not in email or "." not in email:
            return False, "Invalid email format"
        return True, None

    def create_user_dto(self, data):

        return UserDTO(
            username=data['username'],
            password=data['password'],  # TODO: Hashing here
            email=data['email'],
            role=data.get('role', 'user')
        )

    def register_user(self, data):
        required_fields = ['username', 'password', 'email']
        is_valid, error_response, status_code = self.validation_service.validate_request_data(
            data, required_fields)
        if not is_valid:
            return None, error_response, status_code

        is_valid, valid_msg = self.validate_userdata(
            data['username'], data['password'], data['email'])
        if not is_valid:
            return None, valid_msg, 400

        exists, exists_msg = self.user_repository.user_exists(
            data['username'], data['email'])
        if exists:
            return None, exists_msg, 400

        user_dto = self.create_user_dto(data)

        user, message = self.user_repository.create_user(user_dto)

        if not user:
            return None, {'error': message}, 400

        return user, {'message': message, 'user': user.to_dict()}, 201
