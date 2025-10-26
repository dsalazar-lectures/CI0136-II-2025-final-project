from abc import ABC, abstractmethod


class IEncryptionService(ABC):

    @abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abstractmethod
    def verify_password(self, password: str, stored_hash: str) -> bool:
        pass
