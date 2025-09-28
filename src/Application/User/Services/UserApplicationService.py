from src.Application.DTOs.UserDTO import UserDTO
from src.Infrastructure.User.UserRepository import UserRepository
from src.Application.User.Services.ValidationService import ValidationService
from src.Application.User.Services.EncryptionService import EncryptionService


class UserApplicationService:
    def __init__(self):
        self.validation_service = ValidationService()
        self.user_repository = UserRepository()
        self.encryption_service = EncryptionService()

    def create_user_dto(self, data):

        hashed_password = self.encryption_service.hash_password(
            data['password'])

        return UserDTO(
            username=data['username'],
            password=hashed_password,
            email=data['email'],
            role=data.get('role', 'user')
        )

    def register_user(self, data):
        required_fields = ['username', 'password', 'email']
        is_valid, error_response, status_code = self.validation_service.validate_request_data(
            data, required_fields)
        if not is_valid:
            return None, error_response, status_code

        is_valid, valid_msg = self.validation_service.validate_userdata(
            data['username'], data['password'], data['email'])
        if not is_valid:
            return None, {'error': valid_msg}, 400

        exists = self.user_repository.user_exists(
            data['username'], data['email'])
        if exists:
            return None, {'error': "User with this username or email already exists"}, 400

        user_dto = self.create_user_dto(data)

        user, message, status = self.user_repository.create_user(user_dto)

        if not user:
            return None, {'error': message}, status

        return user, {'message': message, 'user': user_dto.to_dict()}, status
