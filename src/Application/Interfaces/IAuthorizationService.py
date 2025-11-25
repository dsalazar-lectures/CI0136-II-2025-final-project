from abc import ABC, abstractmethod
from src.Model.Profiles.Roles import Role


class IAuthorizationService(ABC):
    @abstractmethod
    def is_authorized(self, headers, auth_roles: list[Role]):
        """Check if the user is authorized to perform the given action."""
        pass
