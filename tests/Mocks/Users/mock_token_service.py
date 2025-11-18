from src.Application.Interfaces.ITokenService import ITokenService


class MockTokenService(ITokenService):
    def __init__(self):
        self.tokens = {}
        self.keys = {}

    def generate_token(self, user):
        token = f"mock_token_{user.username}_{user.id}"
        self.tokens[token] = user.id
        return token

    def generate_key(self) -> str:
        return "mock_key"

    def verify_token(self, token):
        return self.tokens.get(token)
