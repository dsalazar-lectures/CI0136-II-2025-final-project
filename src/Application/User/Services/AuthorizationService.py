from src.Application.Interfaces.IAuthorizationService import IAuthorizationService
from src.Application.User.Services.UserApplicationService import UserApplicationService
from src.Application.Interfaces.IProfileApplicationService import (
    IProfileApplicationService,
)
from src.Model.Profiles.Roles import Role
import jwt


class AuthorizationService(IAuthorizationService):
    def __init__(
        self,
        user_app_service: UserApplicationService,
        profile_service: IProfileApplicationService,
    ):
        self.user_app_service = user_app_service
        self.profile_service = profile_service
        
    def get_username_from_token(self, headers):
        token = headers["Authorization"].split(" ")[1]
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            username = payload.get("username")
            if not username:
                return None, {"error": "Invalid token payload"}, 401
            return username, None, None
        except jwt.InvalidTokenError:
            return None, {"error": "Invalid token"}, 401

    def is_authorized(self, headers, auth_roles: list[Role]):
        if "Authorization" not in headers or not headers["Authorization"]:
            return False, {"error": "Authorization header missing"}, 401

        username = None
        username, error_response, status_code = self.get_username_from_token(headers)
        
        if not username:
            return False, error_response, status_code

        user, response, status_code = self.user_app_service.verify_valid_session(
            headers, username
        )
        if not user:
            return False, response, status_code

        profile = self.profile_service.get_profile(user.id)
        if not profile:
            return False, {"error": "Profile not found"}, 404

        if profile.role not in auth_roles:
            return False, {"error": "Unauthorized access"}, 403
        return True, {}, 200
