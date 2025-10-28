import unittest
from src.Application.User.Services.UserApplicationService import UserApplicationService
from src.Application.User.Services.ValidationService import ValidationService
from tests.Mocks.Users.mock_user_repo import MockUserRepository
from tests.Mocks.Users.mock_encryption_service import MockEncryptionService
from tests.Mocks.Users.mock_token_service import MockTokenService
from tests.Mocks.Profile.mock_profile_service import MockProfileService


class testUserApplicationService(unittest.TestCase):
    def setUp(self):
        self.user_repository = MockUserRepository()
        self.encryption_service = MockEncryptionService()
        self.validation_service = ValidationService()
        self.token_service = MockTokenService()
        self.profile_service = MockProfileService()

        self.user_app_service = UserApplicationService(
            user_repository=self.user_repository,
            validation_service=self.validation_service,
            encryption_service=self.encryption_service,
            token_service=self.token_service,
            profile_service=self.profile_service,
        )

    def test_register_user_success(self):
        data = {
            "username": "testUser",
            "password": "Passw@rd123",
            "email": "test@example.com",
        }

        user, response, status_code = self.user_app_service.register_user(data)

        self.assertIsNotNone(user)
        self.assertEqual(status_code, 201)
        self.assertEqual(response["message"], "User created successfully")
        self.assertEqual(response["user"]["username"], "testUser")

    def test_register_user_missing_fields(self):
        data = {
            "username": "testUser"
            # Missing password and email
        }

        user, response, status_code = self.user_app_service.register_user(data)

        self.assertIsNone(user)
        self.assertEqual(status_code, 400)
        self.assertIn("error", response)

    def test_register_user_invalid_data(self):
        data = {"username": "ab", "password": "123", "email": "invalid-email"}

        user, response, status_code = self.user_app_service.register_user(data)

        self.assertIsNone(user)
        self.assertEqual(status_code, 400)
        self.assertIn("error", response)

    def test_register_user_already_exists(self):
        # First registration
        data1 = {
            "username": "testUser",
            "password": "password123",
            "email": "test@example.com",
        }
        self.user_app_service.register_user(data1)

        # Try to register same user again
        data2 = {
            "username": "testUser",
            "password": "differentpassword",
            "email": "different@example.com",
        }

        user, response, status_code = self.user_app_service.register_user(data2)

        self.assertIsNone(user)
        self.assertEqual(status_code, 400)
        self.assertIn("error", response)

    def test_login_user_success(self):
        # First register a user
        register_data = {
            "username": "testUser",
            "password": "Passw@rd123",
            "email": "test@example.com",
        }
        self.user_app_service.register_user(register_data)

        # Then try to login
        login_data = {"username": "testUser", "password": "Passw@rd123"}

        user, response, token, status_code = self.user_app_service.login_user(
            login_data
        )

        self.assertIsNotNone(user)
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "Login successful")

    def test_login_user_invalid_credentials(self):
        login_data = {"username": "nonexistentUser", "password": "password123"}

        user, response, token, status_code = self.user_app_service.login_user(
            login_data
        )

        self.assertIsNone(user)
        self.assertEqual(status_code, 401)
        self.assertIn("error", response)

    def test_login_user_wrong_password(self):
        # Register a user
        register_data = {
            "username": "testUser",
            "password": "password123",
            "email": "test@example.com",
        }
        self.user_app_service.register_user(register_data)

        # Try to login with wrong password
        login_data = {"username": "testUser", "password": "wrongpassword"}

        user, response, token, status_code = self.user_app_service.login_user(
            login_data
        )

        self.assertIsNone(user)
        self.assertEqual(status_code, 401)
        self.assertIn("error", response)

    def test_create_user_dto(self):
        data = {
            "username": "testUser",
            "password": "password123",
            "email": "test@example.com",
            "role": "admin",
        }

        user_dto = self.user_app_service.create_user_dto(data)

        self.assertEqual(user_dto.username, "testUser")
        self.assertEqual(user_dto.email, "test@example.com")
        self.assertEqual(user_dto.role, "admin")
        self.assertTrue(user_dto.password.startswith("hashed_"))

    def test_change_password_success(self):
        # First register a user
        register_data = {
            "username": "testUser",
            "password": "Passw@rd123",
            "email": "test@example.com",
        }
        self.user_app_service.register_user(register_data)

        # Then login
        login_data = {"username": "testUser", "password": "Passw@rd123"}

        user, response, token, status_code = self.user_app_service.login_user(
            login_data
        )

        data = {"old_password": "Passw@rd123", "new_password": "newPassw!rd23"}

        user, msg, status = self.user_app_service.change_password(user, data)

        self.assertIsNotNone(user)
        self.assertEqual(user.password, "hashed_newPassw!rd23")

    def test_change_password_missing_fields(self):
        # First register a user
        register_data = {
            "username": "testUser",
            "password": "Passw@rd123",
            "email": "test@example.com",
        }
        self.user_app_service.register_user(register_data)

        # Then login
        login_data = {"username": "testUser", "password": "Passw@rd123"}

        user, response, token, status_code = self.user_app_service.login_user(
            login_data
        )

        data = {"new_password": "newPassw!rd23"}

        user, msg, status = self.user_app_service.change_password(user, data)

        self.assertIsNone(user)
        self.assertEqual(msg, {"error": "Missing field: old_password"})

    def test_change_password_wrong_password(self):
        # First register a user
        register_data = {
            "username": "testUser",
            "password": "Passw@rd123",
            "email": "test@example.com",
        }
        self.user_app_service.register_user(register_data)

        # Then login
        login_data = {"username": "testUser", "password": "Passw@rd123"}

        user, response, token, status_code = self.user_app_service.login_user(
            login_data
        )

        data = {"old_password": "Passw@r3", "new_password": "newPassw!rd23"}

        user, msg, status = self.user_app_service.change_password(user, data)

        self.assertIsNone(user)
        self.assertEqual(msg, {"error": "Old password is incorrect"})

    def test_change_password_invalid_format(self):
        # First register a user
        register_data = {
            "username": "testUser",
            "password": "Passw@rd123",
            "email": "test@example.com",
        }
        self.user_app_service.register_user(register_data)

        # Then login
        login_data = {"username": "testUser", "password": "Passw@rd123"}

        user, response, token, status_code = self.user_app_service.login_user(
            login_data
        )

        data = {"old_password": "Passw@rd123", "new_password": "newpassw!rd23"}

        user, msg, status = self.user_app_service.change_password(user, data)

        self.assertIsNone(user)
        self.assertEqual(
            msg,
            {
                "error": "The new password does not meet the security requirements (minimum 8 characters, numbers, uppercase, symbols)."
            },
        )


if __name__ == "__main__":
    unittest.main()
