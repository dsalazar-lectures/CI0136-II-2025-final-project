import secrets
import jwt
import datetime
import pytz
import bcrypt


class UserAuthent:

    tz = pytz.timezone("America/Costa_Rica")

    def generate_token(self, user):
        payload = {
            "gen": datetime.datetime.now(self.tz),
            "exp": datetime.datetime.now(self.tz)+datetime.timedelta(minutes=10),
            "sub": user.id,
            "username": user.username
        }

        self.generate_key(user)

        return jwt.encode(payload, user.key, algorithm='HS256')

    def generate_key(self, user):
        user.key = secrets.token_hex(32)

    def hash_password(self, password: str) -> str:
        if isinstance(password, str):
            password = password.encode("utf-8")
        salt = bcrypt.gensalt()  # sin rounds: usa el default de bcrypt
        hashed = bcrypt.hashpw(password, salt)
        return hashed.decode("utf-8")

    def verify_password(self, password: str, stored_hash: str) -> bool:
        if isinstance(password, str):
            password = password.encode("utf-8")
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode("utf-8")
        return bcrypt.checkpw(password, stored_hash)

    def verify_token(self, token):
        return
