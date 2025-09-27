import secrets
import jwt
import datetime
import pytz

class TokenService:

    def __init__(self) -> None:
        self.tz = pytz.timezone("America/Costa_Rica")

    def generate_token(self, user):
        payload = {
            "sub": user.id,
            "username": user.username
        }

        self.generate_key(user)

        return jwt.encode(payload, user.key, algorithm='HS256')
    
    @staticmethod
    def generate_key(user):
        user.key = secrets.token_hex(32)

    @staticmethod
    def verify_token(token):
        pass
