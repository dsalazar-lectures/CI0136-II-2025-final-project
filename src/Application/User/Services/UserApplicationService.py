from src.Application.DTOs.UserDTO import UserDTO
from src.Application.Profiles.Services.ProfileApplicationService import (
    IProfileApplicationService,
)
from src.Application.Interfaces.IUserRepository import IUserRepository
from src.Application.Interfaces.IEncryptionService import IEncryptionService
from src.Application.Interfaces.IValidationService import IValidationService
from src.Application.Interfaces.ITokenService import ITokenService
import jwt


class UserApplicationService:
    def __init__(
        self,
        user_repository: IUserRepository,
        validation_service: IValidationService,
        encryption_service: IEncryptionService,
        token_service: ITokenService,
        profile_service: IProfileApplicationService,
    ):
        self.validation_service = validation_service
        self.user_repository = user_repository
        self.encryption_service = encryption_service
        self.token_service = token_service
        self.profile_service = profile_service

    def create_user_dto(self, data):

        hashed_password = self.encryption_service.hash_password(data["password"])

        return UserDTO(
            id=None,
            username=data["username"],
            password=hashed_password,
            email=data["email"],
            role=data.get("role", "user"),
        )

    def register_user(self, data):
        required_fields = ["username", "password", "email"]
        is_valid, error_response, status_code = (
            self.validation_service.validate_request_data(data, required_fields)
        )
        if not is_valid:
            return None, error_response, status_code

        is_valid, valid_msg = self.validation_service.validate_userdata(
            data["username"], data["email"]
        )
        if not is_valid:
            return None, {"error": valid_msg}, 400

        is_valid, valid_msg = self.validation_service.validate_password_format(
            data["password"]
        )

        if not is_valid:
            return None, {"error": valid_msg}, 400

        exists = self.user_repository.user_exists(data["username"], data["email"])
        if exists:
            return (
                None,
                {"error": "User with this username or email already exists"},
                400,
            )

        user_dto = self.create_user_dto(data)

        user_dto.key = self.token_service.generate_key()

        user, message, status = self.user_repository.create_user(user_dto)

        if not user:
            return None, {"error": message}, status

        self.profile_service.create_profile(user.id)
        return user, {"message": message, "user": user_dto.to_dict()}, status

    def login_user(self, data):
        required_fields = ["username", "password"]
        is_valid, error_response, status_code = (
            self.validation_service.validate_request_data(data, required_fields)
        )
        if not is_valid:
            return None, error_response, None, status_code

        user = self.user_repository.get_user_by_username(data["username"])
        if not user:
            return None, {"error": "Invalid username or password"}, None, 401

        if not self.encryption_service.verify_password(data["password"], user.password):
            return None, {"error": "Invalid username or password"}, None, 401

        token = self.token_service.generate_token(user)

        return user, {"message": "Login successful"}, token, 200

    def change_password(self, user, data):
        required_fields = ["old_password", "new_password"]
        is_valid, error_response, status_code = (
            self.validation_service.validate_request_data(data, required_fields)
        )
        if not is_valid:
            return None, error_response, status_code

        old_password = data["old_password"]
        new_password = data["new_password"]

        # Verify old password
        if not self.encryption_service.verify_password(old_password, user.password):
            return None, {"error": "Old password is incorrect"}, 401

        # Validate new password format
        is_valid, valid_msg = self.validation_service.validate_password_format(
            new_password
        )
        if not is_valid:
            return (
                None,
                {
                    "error": "The new password does not meet the security requirements (minimum 8 characters, numbers, uppercase, symbols)."
                },
                400,
            )

        # Ensure new password is different
        if self.encryption_service.verify_password(new_password, user.password):
            return (
                None,
                {
                    "error": "The new password must be different from the current password."
                },
                400,
            )

        # Hash the new password
        hashed_new_password = self.encryption_service.hash_password(new_password)

        # Update in the database
        success, message, status = self.user_repository.update_password(
            user.username, hashed_new_password
        )
        if not success:
            return None, {"error": message}, status

        return user, {"message": "Password updated successfully"}, 200

    def verify_valid_session(self, header, username):
        # Get user by username
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return None, {"error": "User not found"}, 404

        # Separating the token from 'Bearer'
        token = header["Authorization"].split(" ")[1]

        if self.token_service.verify_token(token, user):
            return user, {"message": "Valid session"}, 200
        else:
            return None, {"error": "Expired session"}, 401

    def regenerate_key(self, headers):
        auth = headers.get("Authorization", "")
        parts = auth.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None, {"error": "Missing or invalid Authorization header"}, 401
        token = parts[1].strip()
        if not token:
            return None, {"error": "Missing token"}, 401

        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            username = payload.get("username")
            if not username:
                return None, {"error": "Invalid token payload"}, 401
        except jwt.InvalidTokenError:
            return None, {"error": "Invalid token"}, 401

        user, resp, status = self.verify_valid_session(headers, username)
        if not user:
            return None, resp, status

        new_key = self.token_service.generate_key()
        ok = self.user_repository.update_user_key(username, new_key)
        if not ok:
            return None, {"error": "Failed to rotate key"}, 500

        return user, {"message": "Key regenerated successfully"}, 200

    def delete_user(self, user_id):
        return self.user_repository.delete_user(user_id)
