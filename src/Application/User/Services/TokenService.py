import secrets
import jwt
import datetime
import pytz
from src.Application.Interfaces.ITokenService import ITokenService

class TokenService(ITokenService):

    def __init__(self) -> None:
        self.tz = pytz.timezone("America/Costa_Rica")

    def generate_token(self, user):
        now = datetime.datetime.now(tz=self.tz)
        payload = {
            "iat": now,
            "exp": now + datetime.timedelta(minutes=60),
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
