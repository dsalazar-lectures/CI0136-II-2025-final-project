from src.Application.Interfaces.IAuthorizationService import IAuthorizationService
from src.Application.User.Services.UserApplicationService import UserApplicationService
from src.Application.Interfaces.IProfileApplicationService import (
    IProfileApplicationService,
)
from src.Model.Profiles.Roles import Role
import jwt
from src.Application.User.Services.EncryptionService import EncryptionService
from src.Application.User.Services.ValidationService import ValidationService
from src.Application.User.Services.TokenService import TokenService
from src.Infrastructure.User.UserRepository import UserRepository
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository
from src.Application.Profiles.Services.ProfileApplicationService import (
    ProfileApplicationService,
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
    
    def is_target_owned(self, request):
        username, _, _ = self.get_username_from_token(
            request.headers
        )
        data = request.get_json()
        return username == data["username"]
    
    def is_superior_user(self, request):
        superior = self.is_target_owned(request) #check if the user is itself
        if not superior:
            username, _, _ = self.get_username_from_token(
                request.headers
            )
            target_name = request.get_json().get("username")
            user = self.user_app_service.user_repository.get_user_by_username(username)
            target = self.user_app_service.user_repository.get_user_by_username(target_name)
            user_profile = self.profile_service.get_profile(user.id)
            target_profile = self.profile_service.get_profile(target.id)
            
            if user_profile.role == Role.GOD:
                superior = True
            elif user_profile.role == Role.ADMIN:
                if target_profile.role == Role.USER:
                    superior = True
        return superior
    
def create_default_auth_service() -> AuthorizationService:
    user_repository = UserRepository()
    validation_service = ValidationService()
    encryption_service = EncryptionService()
    token_service = TokenService()
    profile_service = ProfileApplicationService(profile_repository=ProfileRepository())
    user_app_service = UserApplicationService(
        user_repository=user_repository,
        validation_service=validation_service,
        encryption_service=encryption_service,
        token_service=token_service,
        profile_service=profile_service,
    )
    auth_service = AuthorizationService(user_app_service, profile_service)