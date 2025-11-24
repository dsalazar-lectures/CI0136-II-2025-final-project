import unittest
from unittest.mock import Mock
from src.Infrastructure.User.PasswordResetTokenRepository import (
    PasswordResetTokenRepository,
)


class TestPasswordResetTokenRepository(unittest.TestCase):
    def setUp(self):
        self.mock_csv = Mock()
        self.repo = PasswordResetTokenRepository()
        self.repo.token_csv = self.mock_csv  # replace real csv with mock

    def test_create_token(self):
        self.repo.create_token("1", "abc", "2025-01-01")
        self.mock_csv.create_token.assert_called_once()

    def test_get_valid_token(self):
        fake = Mock()
        self.mock_csv.get_valid_token.return_value = fake

        result = self.repo.get_valid_token("abc")
        self.assertEqual(result, fake)

    def test_invalidate_token(self):
        self.repo.invalidate_token("abc")
        self.mock_csv.invalidate_token.assert_called_once_with("abc")

    def test_invalidate_all_user_tokens(self):
        self.repo.invalidate_all_user_tokens("1")
        self.mock_csv.invalidate_all_user_tokens.assert_called_once_with("1")
