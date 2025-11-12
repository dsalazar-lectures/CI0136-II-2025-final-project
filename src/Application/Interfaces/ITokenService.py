from abc import ABC, abstractmethod


class ITokenService(ABC):

    @abstractmethod
    def generate_token(self, user):
        pass

    @abstractmethod
    def generate_key(self) -> str: ...

    @abstractmethod
    def verify_token(self, token, user):
        pass
