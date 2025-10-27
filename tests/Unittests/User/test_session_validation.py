import unittest
import jwt
import pytz
import datetime

from src.Application.User.Services.UserApplicationService import UserApplicationService
from src.Application.User.Services.ValidationService import ValidationService
from tests.Mocks.Users.mock_user_repo import MockUserRepository
from tests.Mocks.Users.mock_encryption_service import MockEncryptionService
from src.Application.User.Services.TokenService import TokenService


class TestSessionService(unittest.TestCase):

    def setUp(self):
        self.user_repository = MockUserRepository()
        self.encryption_service = MockEncryptionService()
        self.validation_service = ValidationService()
        self.token_service = TokenService()

        self.user_app_service = UserApplicationService(
            user_repository=self.user_repository,
            validation_service=self.validation_service,
            encryption_service=self.encryption_service,
            token_service=self.token_service,
        )

        self.tz = pytz.timezone("America/Costa_Rica")

    def test_valid_token(self):
        # register a user
        register_data = {
            "username": "testUser",
            "password": "Passw@rd123",
            "email": "test@example.com",
        }
        self.user_app_service.register_user(register_data)

        # Then login
        login_data = {"username": "testUser", "password": "Passw@rd123"}

        user, response, status_code = self.user_app_service.login_user(login_data)

        header = {"Authorization": f"Bearer {user.token}"}

        user, msg, status_code = self.user_app_service.verify_valid_session(
            header, user.username
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

        expired_token = jwt.encode(
            {"exp": datetime.datetime.now(tz=self.tz) - datetime.timedelta(minutes=5)},
            "mock_key",
            algorithm="HS256",
        )

        header = {"Authorization": f"Bearer {expired_token}"}

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
