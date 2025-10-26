from src.Application.DTOs.UserDTO import UserDTO
from src.Application.Interfaces.IUserRepository import IUserRepository
from src.Application.User.Services.ValidationService import ValidationService
from src.Application.User.Services.EncryptionService import EncryptionService
from src.Application.User.Services.TokenService import TokenService

class UserApplicationService:
    def __init__(self, user_repository: IUserRepository):
        self.validation_service = ValidationService()
        self.user_repository = user_repository
        self.encryption_service = EncryptionService()
        self.token_service = TokenService()

    def create_user_dto(self, data):

        hashed_password = self.encryption_service.hash_password(
            data['password'])

        return UserDTO(
            id=None,
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

    def login_user(self, data):
        required_fields = ['username', 'password']
        is_valid, error_response, status_code = self.validation_service.validate_request_data(
            data, required_fields)
        if not is_valid:
            return None, error_response, status_code

        user = self.user_repository.get_user_by_username(data['username'])
        if not user:
            return None, {'error': "Invalid username or password"}, 401

        if not self.encryption_service.verify_password(data['password'], user.password):
            return None, {'error': "Invalid username or password"}, 401

        token = self.token_service.generate_token(user)

        return user, {'message': "Login successful", 'token': token}, 200
    
    def change_password(self, username, data):
        required_fields = ['old_password', 'new_password']
        is_valid, error_response, status_code = self.validation_service.validate_request_data(
            data, required_fields)
        if not is_valid:
            return None, error_response, status_code

        old_password = data["old_password"]
        new_password = data["new_password"]

        # Get user by username
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return None, {'error': "User not found"}, 404

        # Verify old password
        if not self.encryption_service.verify_password(old_password, user.password):
            return None, {'error': "Old password is incorrect"}, 401

        # Validate new password format
        is_valid, valid_msg = self.validation_service.validate_password_format(new_password)
        if not is_valid:
            return None, {
                'error': 'The new password does not meet the security requirements (minimum 8 characters, numbers, uppercase, symbols).'
            }, 400

        # Ensure new password is different
        if self.encryption_service.verify_password(new_password, user.password):
            return None, {'error': 'The new password must be different from the current password.'}, 400

        # Hash the new password
        hashed_new_password = self.encryption_service.hash_password(new_password)

        # Update in the database
        success, message, status = self.user_repository.update_password(username, hashed_new_password)
        if not success:
            return None, {'error': message}, status

        return user, {'message': "Password updated successfully"}, 200
    
    def change_email(self, username, data):
        # Required fields
        required_fields = ['old_email', 'new_email', 'password']
        is_valid, error_response, status_code = self.validation_service.validate_request_data(
            data, required_fields)
        if not is_valid:
            return None, error_response, status_code

        old_email = data['old_email']
        new_email = data['new_email']
        password = data['password']

        # Get user by username
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return None, {'error': "User not found"}, 404

        # Verify password
        if not self.encryption_service.verify_password(password, user.password):
            return None, {'error': "Password is incorrect"}, 401

        # Verify old email matches
        if user.email != old_email:
            return None, {'error': "Old email does not match our records"}, 400

        # Validate new email format
        is_valid, valid_msg = self.validation_service.validate_email_format(new_email)
        if not is_valid:
            return None, {'error': "New email is not valid"}, 400

        # Ensure new email is different
        if new_email == user.email:
            return None, {'error': "New email must be different from the current email"}, 400

        # Update in the database
        success, message, status = self.user_repository.update_email(username, new_email)
        if not success:
            return None, {'error': message}, status

        return user, {'message': "Email updated successfully"}, 200