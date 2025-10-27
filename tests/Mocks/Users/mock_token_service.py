from src.Application.Interfaces.ITokenService import ITokenService


class MockTokenService(ITokenService):
    def __init__(self):
        self.tokens = {}
        self.keys = {}

    def generate_token(self, user):
        token = f"mock_token_{user.username}_{user.id}"
        self.tokens[token] = user.id
        return token

    def generate_key(self, user):
        key = f"mock_key_{user.username}"
        user.key = key
        self.keys[user.username] = key

    def verify_token(self, token, user):
        return self.tokens.get(token)
