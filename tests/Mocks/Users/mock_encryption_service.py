from src.Application.Interfaces.IEncryptionService import IEncryptionService


class MockEncryptionService(IEncryptionService):
    def __init__(self):
        self.hashes = {}

    def hash_password(self, password: str) -> str:
        hashed = f"hashed_{password}"
        self.hashes[hashed] = password
        return hashed

    def verify_password(self, password: str, stored_hash: str) -> bool:
        return self.hashes.get(stored_hash) == password
