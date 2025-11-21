from src.Application.DTOs.UserDTO import UserDTO
from src.Application.Interfaces.IUserRepository import IUserRepository
from Application.Interfaces.IPasswordResetTokenRepository import IPasswordResetTokenRepository
from src.Application.User.Services.ValidationService import ValidationService
from src.Application.User.Services.EncryptionService import EncryptionService
from src.Application.User.Services.TokenService import TokenService
from src.Application.User.Services.PasswordResetTokenService import PasswordResetTokenService

class UserApplicationService:
    def __init__(self, user_repository: IUserRepository, token_repository: IPasswordResetTokenRepository = None):
        self.validation_service = ValidationService()
        self.user_repository = user_repository
        self.encryption_service = EncryptionService()
        self.token_service = TokenService()
        if token_repository:
            self.password_reset_service = PasswordResetTokenService(token_repository)
        else:
            self.password_reset_service = None

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
    
    def request_password_reset(self, data):
        # Requests a password reset link for the given email
        if not self.password_reset_service:
            return None, {'error': "Password reset service not available"}, 500

        required_fields = ['email']
        is_valid, error_response, status_code = self.validation_service.validate_request_data(
            data, required_fields)
        if not is_valid:
            return None, error_response, status_code

        user = self.user_repository.get_user_by_email(data['email'])
        if not user:
            return None, {'message': "If the email exists, a password reset link has been sent"}, 200

        reset_token = self.password_reset_service.generate_reset_token(str(user.id))
        reset_link = f"http://localhost:5000/reset-password?token={reset_token}"

        try:
            from src.Services.EmailService import send_email
            send_email(
                sender="noreply@yourapp.com",
                recipient=user.email,
                subject="Password Reset Request",
                contents=f"Reset link: {reset_link}"
            )
        except Exception as e:
            return None, {'error': "Failed to send reset email"}, 500

        return None, {'message': "If the email exists, a password reset link has been sent"}, 200

    def reset_password(self, data):
        # Resets the user's password using the provided token and new password
        if not self.password_reset_service:
            return None, {'error': "Password reset service not available"}, 500

        required_fields = ['token', 'new_password']
        is_valid, error_response, status_code = self.validation_service.validate_request_data(
            data, required_fields)
        if not is_valid:
            return None, error_response, status_code

        token = data['token']
        new_password = data['new_password']

        is_valid_token, user_id_or_error = self.password_reset_service.verify_reset_token(token)
        if not is_valid_token:
            return None, {'error': user_id_or_error}, 400

        is_valid, valid_msg = self.validation_service.validate_password_format(new_password)
        if not is_valid:
            return None, {'error': valid_msg}, 400

        hashed_new_password = self.encryption_service.hash_password(new_password)
        success, message, status = self.user_repository.update_password_by_id(
            user_id_or_error, hashed_new_password)
        
        if not success:
            return None, {'error': message}, status

        self.password_reset_service.invalidate_token(token)
        return None, {'message': "Password reset successfully"}, 200