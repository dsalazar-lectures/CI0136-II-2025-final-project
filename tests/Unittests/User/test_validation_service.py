import unittest
from src.Application.User.Services.ValidationService import ValidationService


class TestValidationService(unittest.TestCase):
    def setUp(self):
        self.validation_service = ValidationService()

    def test_validate_request_data_success(self):
        data = {"username": "test", "password": "123456", "email": "test@example.com"}
        required_fields = ["username", "password", "email"]

        is_valid, error, status = self.validation_service.validate_request_data(
            data, required_fields
        )

        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_request_data_missing_field(self):
        data = {"username": "test", "password": "123456"}
        required_fields = ["username", "password", "email"]

        is_valid, error, status = self.validation_service.validate_request_data(
            data, required_fields
        )

        self.assertFalse(is_valid)
        self.assertIn("error", error)
        self.assertEqual(status, 400)

    def test_validate_userdata_success(self):
        is_valid, error = self.validation_service.validate_userdata(
            "testuser", "password123", "test@example.com"
        )

        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_userdata_invalid_email(self):
        is_valid, error = self.validation_service.validate_userdata(
            "testuser", "password123", "invalid-email"
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, "Invalid email format")

    def test_validate_userdata_short_username(self):
        is_valid, error = self.validation_service.validate_userdata(
            "ab", "password123", "test@example.com"
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, "Username must be at least 3 characters long")

    def test_validate_userdata_short_password(self):
        is_valid, error = self.validation_service.validate_userdata(
            "testuser", "123", "test@example.com"
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, "Password must be at least 6 characters long")


if __name__ == "__main__":
    unittest.main()
