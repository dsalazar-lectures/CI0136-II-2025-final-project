from src.Application.Interfaces.ITokenService import ITokenService


class MockTokenService(ITokenService):
    def __init__(self):
        self.tokens = {}
        self.counter = 0

    def generate_token(self, user):
        token = f"mock_token_{user.username}_{user.id}"
        self.tokens[token] = user.id
        return token

    def generate_key(self) -> str:
        self.counter += 1
        return f"mock_key_{self.counter}"

    def verify_token(self, token):
        return self.tokens.get(token)
