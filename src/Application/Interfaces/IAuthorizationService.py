from abc import ABC, abstractmethod


class IAuthorizationService(ABC):
    @abstractmethod
    def is_authorized(self, username: str, headers, auth_role):
        """Check if the user is authorized to perform the given action."""
        pass
