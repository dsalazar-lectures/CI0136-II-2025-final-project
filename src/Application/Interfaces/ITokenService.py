from abc import ABC, abstractmethod


class ITokenService(ABC):

    @abstractmethod
    def generate_token(self, user):
        pass

    @abstractmethod
    def generate_key(self, user):
        pass

    @abstractmethod
    def verify_token(self, token):
        pass
