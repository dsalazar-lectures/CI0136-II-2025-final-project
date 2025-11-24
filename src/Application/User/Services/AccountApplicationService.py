import jwt
from src.Application.Interfaces.IUserRepository import IUserRepository
from src.Application.Interfaces.ITokenService import ITokenService
from src.Application.Profiles.Services.ProfileApplicationService import (
    IProfileApplicationService,
)
from src.Shared.Logs.custom_logger import CustomLogger

account_logger = CustomLogger(name="Account")


class AccountApplicationService:
    def __init__(
        self,
        user_repository: IUserRepository,
        profile_service: IProfileApplicationService,
        token_service: ITokenService,
    ):
        self.user_repository = user_repository
        self.profile_service = profile_service
        self.token_service = token_service

    def _verify_valid_session(self, headers, username):
        """Auxiliary method to verify if a session is valid based on headers and username.
        (similar to UserApplicationService)"""
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return None, {"error": "User not found"}, 404

        token = headers["Authorization"].split(" ")[1]

        if self.token_service.verify_token(token, user):
            return user, {"message": "Valid session"}, 200
        else:
            return None, {"error": "Expired session"}, 401

    def delete_user_account(self, headers, username_to_delete):
        # Validate and extract token
        auth = headers.get("Authorization", "")
        parts = auth.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            account_logger.log(
                "error",
                username_to_delete,
                None,
                "ACCOUNT_DELETE_FAIL",
                None,
                "Missing or invalid Authorization header",
            )
            return None, {"error": "Missing or invalid Authorization header"}, 401

        token = parts[1].strip()

        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            username = payload.get("username")
            if not username:
                account_logger.log(
                    "error",
                    username_to_delete,
                    None,
                    "ACCOUNT_DELETE_FAIL",
                    None,
                    "Token payload missing username",
                )
                return None, {"error": "Invalid token payload"}, 401
        except jwt.InvalidTokenError:
            account_logger.log(
                "error",
                username_to_delete,
                None,
                "ACCOUNT_DELETE_FAIL",
                None,
                "Failed to decode token",
            )
            return None, {"error": "Invalid token"}, 401

        # Verify session
        user, resp, status = self._verify_valid_session(headers, username)
        if not user:
            return None, resp, status

        # Search for the user to delete
        user_to_delete = self.user_repository.get_user_by_username(username_to_delete)
        if not user_to_delete:
            account_logger.log(
                "warning",
                username_to_delete,
                None,
                "ACCOUNT_DELETE_FAIL",
                None,
                "User to delete not found",
            )
            return None, {"error": "User not found"}, 404

        # Store profile before deletion
        profile_to_delete = self.profile_service.get_profile(user_to_delete.id)
        if not profile_to_delete:
            account_logger.log(
                "warning",
                user_to_delete.username,
                user_to_delete.role,
                "PROFILE_DELETE_FAIL",
                user_to_delete.id,
                "User profile to delete not found",
            )
            return None, {"error": "User profile not found"}, 404

        # Delete user profile
        profile_deleted = self.profile_service.delete_profile(user_to_delete.id)
        if not profile_deleted:
            account_logger.log(
                "error",
                user_to_delete.username,
                user_to_delete.role,
                "PROFILE_DELETE_FAIL",
                user_to_delete.id,
                "Failed to delete user profile",
            )
            return None, {"error": "Failed to delete user profile"}, 500

        if profile_deleted:
            account_logger.log(
                "info",
                user_to_delete.username,
                user_to_delete.role,
                "PROFILE_DELETE_SUCCESS",
                user_to_delete.id,
                "Profile deleted successfully",
            )

            # Delete user account
            user_deleted = self.user_repository.delete_user(user_to_delete.id)
            if not user_deleted:
                account_logger.log(
                    "error",
                    user_to_delete.username,
                    user_to_delete.role,
                    "ACCOUNT_DELETE_FAIL",
                    user_to_delete.id,
                    "User deletion failed, restoring profile",
                )

                # Rollback profile deletion if user deletion fails
                self.profile_service.restore_profile(
                    user_to_delete.id, profile_to_delete.favorite_foods
                )

                account_logger.log(
                    "info",
                    user_to_delete.username,
                    user_to_delete.role,
                    "PROFILE_RESTORE_SUCCESS",
                    user_to_delete.id,
                    "Profile restored successfully after failed account deletion",
                )
                return None, {"error": "Failed to delete user account"}, 500

        account_logger.log(
            "info",
            user_to_delete.username,
            user_to_delete.role,
            "ACCOUNT_DELETE_SUCCESS",
            user_to_delete.id,
            "User account deleted successfully",
        )

        return (
            user_to_delete,
            {"message": "User account and profile deleted successfully"},
            200,
        )
