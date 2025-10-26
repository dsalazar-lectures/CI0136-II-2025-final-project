from src.Application.DTOs.UserDTO import UserDTO
from src.Application.Interfaces.IUserRepository import IUserRepository
from src.Application.Interfaces.IEncryptionService import IEncryptionService
from src.Application.Interfaces.IValidationService import IValidationService
from src.Application.Interfaces.ITokenService import ITokenService


class UserApplicationService:
    def __init__(
        self,
        user_repository: IUserRepository,
        validation_service: IValidationService,
        encryption_service: IEncryptionService,
        token_service: ITokenService,
    ):
        self.validation_service = validation_service
        self.user_repository = user_repository
        self.encryption_service = encryption_service
        self.token_service = token_service

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
            data["username"], data["password"], data["email"]
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

        user, message, status = self.user_repository.create_user(user_dto)

        if not user:
            return None, {"error": message}, status

        self.user_repository.create_user_profile(user.id)
        return user, {"message": message, "user": user_dto.to_dict()}, status

    def login_user(self, data):
        required_fields = ["username", "password"]
        is_valid, error_response, status_code = (
            self.validation_service.validate_request_data(data, required_fields)
        )
        if not is_valid:
            return None, error_response, status_code

        user = self.user_repository.get_user_by_username(data["username"])
        if not user:
            return None, {"error": "Invalid username or password"}, 401

        if not self.encryption_service.verify_password(data["password"], user.password):
            return None, {"error": "Invalid username or password"}, 401

        token = self.token_service.generate_token(user)

        return user, {"message": "Login successful", "token": token}, 200
