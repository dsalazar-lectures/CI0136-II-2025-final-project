# Interface for Password Reset Token Repository
from abc import ABC, abstractmethod
from typing import Optional
import datetime

class IPasswordResetTokenRepository(ABC):
    @abstractmethod
    # Persist a token for user_id that expires at expires_at.
    def create_token(self, user_id: str, token: str, expires_at: datetime.datetime):
        pass

    # Retrieve the token record if it exists and is still valid.
    # Return None if the token does not exist, is expired, or has been invalidated.
    @abstractmethod
    def get_valid_token(self, token: str) -> Optional[object]:
        pass

    # Invalidate a specific token.
    @abstractmethod
    def invalidate_token(self, token: str):
        pass

    #Invalidate all tokens for a specific user.
    @abstractmethod
    def invalidate_all_user_tokens(self, user_id: str):
        pass
