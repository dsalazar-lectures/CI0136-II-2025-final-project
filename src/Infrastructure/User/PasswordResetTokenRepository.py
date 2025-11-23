from Application.Interfaces.IPasswordResetTokenRepository import (
    IPasswordResetTokenRepository,
)
from src.Database.User.PasswordResetTokenCSV import PasswordResetTokenCSV
import datetime


class PasswordResetTokenRepository(IPasswordResetTokenRepository):
    def __init__(self, csv_file_path="password_reset_tokens.csv"):
        self.token_csv = PasswordResetTokenCSV(csv_file_path)

    def create_token(self, user_id: str, token: str, expires_at: datetime.datetime):
        self.token_csv.create_token(user_id, token, expires_at)

    def get_valid_token(self, token: str):
        return self.token_csv.get_valid_token(token)

    def invalidate_token(self, token: str):
        self.token_csv.invalidate_token(token)

    def invalidate_all_user_tokens(self, user_id: str):
        self.token_csv.invalidate_all_user_tokens(user_id)