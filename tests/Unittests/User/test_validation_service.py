import unittest
from src.Application.User.Services.ValidationService import ValidationService


class TestValidationService(unittest.TestCase):
    def setUp(self):
        self.validation_service = ValidationService()

        self.generic_msg = (
            "error: The new password does not meet the security requirements "
            "(minimum 8 characters and include at least one number, one uppercase letter, "
            'and one special character (e.g. !@#$%^&*(),.?":{}|<>).'
        )

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
            "testuser", "test@example.com"
        )

        self.assertTrue(is_valid)
        self.assertIsNone(error)

    def test_validate_userdata_invalid_email(self):
        is_valid, error = self.validation_service.validate_userdata(
            "testuser", "invalid-email"
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, "Invalid email format")

    def test_validate_userdata_short_username(self):
        is_valid, error = self.validation_service.validate_userdata(
            "ab", "test@example.com"
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, "Username must be at least 3 characters long")

    def test_validate_password_format_success(self):
        is_valid, msg = self.validation_service.validate_password_format(
            "Validp4ssw!rd"
        )

        self.assertTrue(is_valid)
        self.assertEqual(msg, "Password format is valid.")

    def test_validate_short_password(self):
        is_valid, error = self.validation_service.validate_password_format("123")

        self.assertFalse(is_valid)
        self.assertEqual(error, self.generic_msg)

    def test_validate_password_in_lower_case(self):
        is_valid, error = self.validation_service.validate_password_format(
            "invalidp4ss!rd"
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, self.generic_msg)

    def test_validate_password_without_num(self):
        is_valid, error = self.validation_service.validate_password_format(
            "Invalidpass!rd"
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, self.generic_msg)

    def test_validate_password_without_special_char(self):
        is_valid, error = self.validation_service.validate_password_format(
            "Invalidp4sswrd"
        )

        self.assertFalse(is_valid)
        self.assertEqual(error, self.generic_msg)


if __name__ == "__main__":
    unittest.main()
