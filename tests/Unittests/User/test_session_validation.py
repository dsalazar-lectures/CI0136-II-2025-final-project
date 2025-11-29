import unittest
from unittest.mock import patch

from src.Application.User.Services.UserApplicationService import UserApplicationService
from src.Application.User.Services.ValidationService import ValidationService
from tests.Mocks.Users.mock_user_repo import MockUserRepository
from tests.Mocks.Users.mock_encryption_service import MockEncryptionService
from tests.Mocks.Users.mock_token_service import MockTokenService
from tests.Mocks.Profile.mock_profile_service import MockProfileService


class MockPasswordResetTokenService:
    def generate_reset_token(self, user_id):
        return "mock_token"

    def verify_reset_token(self, token):
        return False, "Mock error"

    def invalidate_token(self, token):
        pass

    def invalidate_all_user_tokens(self, user_id):
        pass


class TestSessionService(unittest.TestCase):

    def setUp(self):
        self.user_repository = MockUserRepository()
        self.encryption_service = MockEncryptionService()
        self.validation_service = ValidationService()
        self.token_service = MockTokenService()
        self.profile_service = MockProfileService()

        self.password_reset_service = MockPasswordResetTokenService()

        self.user_app_service = UserApplicationService(
            user_repository=self.user_repository,
            validation_service=self.validation_service,
            encryption_service=self.encryption_service,
            token_service=self.token_service,
            profile_service=self.profile_service,
            password_reset_service=MockPasswordResetTokenService(),
        )

    def test_valid_token(self):
        # register a user
        register_data = {
            "username": "testUser",
            "password": "Passw@rd123",
            "email": "test@example.com",
        }
        self.user_app_service.register_user(register_data)

        header = {"Authorization": "Bearer fake_token"}

        with patch.object(
            self.user_app_service.token_service, "verify_token", return_value=True
        ):
            user, msg, status_code = self.user_app_service.verify_valid_session(
                header, "testUser"
            )

        self.assertIsNotNone(user)

    def test_expired_token(self):
        # register a user
        register_data = {
            "username": "testUser",
            "password": "Passw@rd123",
            "email": "test@example.com",
        }

        user, response, status_code = self.user_app_service.register_user(register_data)

        header = {"Authorization": "Bearer fake_token"}

        with patch.object(
            self.user_app_service.token_service, "verify_token", return_value=False
        ):
            user, msg, status_code = self.user_app_service.verify_valid_session(
                header, "testUser"
            )

        self.assertIsNone(user)
        self.assertEqual(msg, {"error": "Expired session"})

    def test_user_not_found(self):
        header = {"Authorization": "Bearer sometoken"}

        user, msg, status_code = self.user_app_service.verify_valid_session(
            header, "unregistereUser"
        )

        self.assertIsNone(user)
        self.assertEqual(msg, {"error": "User not found"})


if __name__ == "__main__":
    unittest.main()
