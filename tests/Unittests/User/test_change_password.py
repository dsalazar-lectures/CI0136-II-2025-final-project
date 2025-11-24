import unittest
from unittest.mock import Mock
from src.Application.User.Services.UserApplicationService import UserApplicationService


class TestChangePassword(unittest.TestCase):
    def setUp(self):
        # Mocks
        self.user_repo = Mock()
        self.validation = Mock()
        self.encryption = Mock()
        self.token_service = Mock()
        self.profile_service = Mock()

        # Service
        self.service = UserApplicationService(
            self.user_repo,
            self.validation,
            self.encryption,
            self.token_service,
            self.profile_service
        )

        # Fake user
        self.user = Mock()
        self.user.username = "alice"
        self.user.password = "hashed_old_pw"
        self.user.email = "alice@example.com"

    def test_change_password_old_password_wrong(self):
        self.validation.validate_request_data.return_value = (True, None, None)
        self.encryption.verify_password.return_value = False  # old password wrong

        user, resp, status = self.service.change_password(
            self.user,
            {"old_password": "wrong", "new_password": "NewPass!23"}
        )

        self.assertIsNone(user)
        self.assertEqual(status, 401)
        self.assertIn("Old password is incorrect", resp["error"])

    def test_change_password_new_password_invalid_format(self):
        self.validation.validate_request_data.return_value = (True, None, None)
        self.encryption.verify_password.side_effect = [True, False]  
        # first: old matches, second: new != old
        self.validation.validate_password_format.return_value = (False, "bad format")

        user, resp, status = self.service.change_password(
            self.user,
            {"old_password": "correct", "new_password": "short"}
        )

        self.assertIsNone(user)
        self.assertEqual(status, 400)

    def test_change_password_new_equals_old(self):
        self.validation.validate_request_data.return_value = (True, None, None)
        # old password correct
        self.encryption.verify_password.side_effect = [True, True]  
        # second True means "new password verifies as same as old"

        self.validation.validate_password_format.return_value = (True, None)

        user, resp, status = self.service.change_password(
            self.user,
            {"old_password": "oldpw", "new_password": "oldpw"}
        )

        self.assertIsNone(user)
        self.assertEqual(status, 400)
        self.assertIn("must be different", resp["error"])

    def test_change_password_update_failed(self):
        self.validation.validate_request_data.return_value = (True, None, None)
        self.encryption.verify_password.side_effect = [True, False]
        self.validation.validate_password_format.return_value = (True, None)
        self.encryption.hash_password.return_value = "hashed_new"

        self.user_repo.update_password.return_value = (False, "DB error", 500)

        user, resp, status = self.service.change_password(
            self.user,
            {"old_password": "correct", "new_password": "NewPass!23"}
        )

        self.assertIsNone(user)
        self.assertEqual(status, 500)
        self.assertIn("DB error", resp["error"])

    def test_change_password_success(self):
        self.validation.validate_request_data.return_value = (True, None, None)
        self.encryption.verify_password.side_effect = [True, False]  
        self.validation.validate_password_format.return_value = (True, None)
        self.encryption.hash_password.return_value = "hashed_new"

        self.user_repo.update_password.return_value = (True, "ok", 200)

        user, resp, status = self.service.change_password(
            self.user,
            {"old_password": "correct", "new_password": "NewPass!23"}
        )

        self.assertEqual(status, 200)
        self.assertIsNotNone(user)
        self.assertIn("Password updated successfully", resp["message"])
