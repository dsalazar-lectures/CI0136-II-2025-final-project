import secrets
import datetime
import pytz
from Application.Interfaces.IPasswordResetTokenRepository import (
    IPasswordResetTokenRepository,
)


class PasswordResetTokenService:
    def __init__(self, token_repository: IPasswordResetTokenRepository) -> None:
        self.tz = pytz.timezone("America/Costa_Rica")
        self.token_repository = token_repository

    # Generate a password reset token for a user
    def generate_reset_token(self, user_id: str) -> str:
        # Generate a secure random token
        token = secrets.token_urlsafe(32)

        # Calculates expiration time (1 hour from now)
        expires_at = datetime.datetime.now(tz=self.tz) + datetime.timedelta(hours=1)

        # Store the token in the repository
        self.token_repository.create_token(
            user_id=user_id, token=token, expires_at=expires_at
        )

        return token

    def verify_reset_token(self, token: str) -> tuple[bool, str]:
        # Verify if a password reset token is valid
        # Obtain token data from repository
        token_data = self.token_repository.get_valid_token(token)

        # If no token found or already used
        if not token_data:
            return False, "Invalid or expired token"

        # If token is expired
        if token_data.expires_at < datetime.datetime.now(tz=self.tz):
            # Invalidar token expirado
            self.token_repository.invalidate_token(token)
            return False, "Token has expired"

        # If token is valid
        return True, token_data.user_id

    def invalidate_token(self, token: str):
        # invalidate a specific password reset token
        self.token_repository.invalidate_token(token)

    def invalidate_all_user_tokens(self, user_id: str):
        # invalidate all password reset tokens for a specific user
        self.token_repository.invalidate_all_user_tokens(user_id)