import unittest
from unittest.mock import Mock
from src.Application.User.Services.AuthorizationService import AuthorizationService
from src.Model.Profiles.Roles import Role
from src.Model.Profiles.Profiles import Profile
from src.Application.DTOs.UserDTO import UserDTO


class TestAuthorizationService(unittest.TestCase):
    def setUp(self):
        self.mock_user_app_service = Mock()
        self.mock_profile_service = Mock()
        self.auth_service = AuthorizationService(
            user_app_service=self.mock_user_app_service,
            profile_service=self.mock_profile_service,
        )

    def test_is_authorized_missing_auth_header(self):
        data = {"username": "testuser"}
        headers = {}
        auth_role = Role.ADMIN

        is_auth, response, status_code = self.auth_service.is_authorized(
            data, headers, auth_role
        )

        self.assertFalse(is_auth)
        self.assertEqual(status_code, 401)
        self.assertIn("Authorization header missing", response["error"])

    def test_is_authorized_empty_auth_header(self):
        data = {"username": "testuser"}
        headers = {"Authorization": ""}
        auth_role = Role.ADMIN

        is_auth, response, status_code = self.auth_service.is_authorized(
            data, headers, auth_role
        )

        self.assertFalse(is_auth)
        self.assertEqual(status_code, 401)
        self.assertIn("Authorization header missing", response["error"])

    def test_is_authorized_invalid_request_data(self):
        data = {"username": "testuser"}
        headers = {"Authorization": "Bearer token"}
        auth_role = Role.ADMIN

        self.mock_user_app_service.validation_service.validate_request_data.return_value = (
            False,
            {"error": "Invalid data"},
            400,
        )

        is_auth, response, status_code = self.auth_service.is_authorized(
            data, headers, auth_role
        )

        self.mock_user_app_service.validation_service.validate_request_data.assert_called_once_with(
            data, ["username"]
        )
        self.assertFalse(is_auth)
        self.assertEqual(status_code, 400)
        self.assertIn("Invalid data", response["error"])

    def test_is_authorized_invalid_session(self):
        data = {"username": "testuser"}
        headers = {"Authorization": "Bearer token"}
        auth_role = Role.ADMIN

        self.mock_user_app_service.validation_service.validate_request_data.return_value = (
            True,
            None,
            None,
        )
        self.mock_user_app_service.verify_valid_session.return_value = (
            None,
            {"error": "Expired session"},
            401,
        )

        is_auth, response, status_code = self.auth_service.is_authorized(
            data, headers, auth_role
        )

        self.mock_user_app_service.verify_valid_session.assert_called_once_with(
            headers, data["username"]
        )
        self.assertFalse(is_auth)
        self.assertEqual(status_code, 401)
        self.assertIn("Expired session", response["error"])

    def test_is_authorized_profile_not_found(self):
        data = {"username": "testuser"}
        headers = {"Authorization": "Bearer token"}
        auth_role = Role.ADMIN

        self.mock_user_app_service.validation_service.validate_request_data.return_value = (
            True,
            None,
            None,
        )
        user = UserDTO(1, "testuser", "hashedpwd", "mock@gmail.com")
        self.mock_user_app_service.verify_valid_session.return_value = (
            user,
            {"message": "Valid session"},
            200,
        )
        self.mock_profile_service.get_profile.return_value = None

        is_auth, response, status_code = self.auth_service.is_authorized(
            data, headers, auth_role
        )

        self.mock_profile_service.get_profile.assert_called_once_with(user.id)
        self.assertFalse(is_auth)
        self.assertEqual(status_code, 404)
        self.assertIn("Profile not found", response["error"])

    def test_is_authorized_no_access(self):
        data = {"username": "testuser"}
        headers = {"Authorization": "Bearer token"}
        auth_role = Role.ADMIN

        self.mock_user_app_service.validation_service.validate_request_data.return_value = (
            True,
            None,
            None,
        )
        user = UserDTO(1, "testuser", "hashedpwd", "mock@gmail.com")
        self.mock_user_app_service.verify_valid_session.return_value = (
            user,
            {"message": "Valid session"},
            200,
        )
        self.mock_profile_service.get_profile.return_value = Profile(1, role=Role.USER)

        is_auth, response, status_code = self.auth_service.is_authorized(
            data, headers, auth_role
        )

        self.assertFalse(is_auth)
        self.assertEqual(status_code, 403)
        self.assertIn("Unauthorized access", response["error"])

    def test_is_authorized_happy_path(self):
        data = {"username": "testuser"}
        headers = {"Authorization": "Bearer token"}
        auth_role = Role.ADMIN

        self.mock_user_app_service.validation_service.validate_request_data.return_value = (
            True,
            None,
            None,
        )
        user = UserDTO(1, "testuser", "hashedpwd", "mock@gmail.com")
        self.mock_user_app_service.verify_valid_session.return_value = (
            user,
            {"message": "Valid session"},
            200,
        )
        self.mock_profile_service.get_profile.return_value = Profile(1, role=Role.ADMIN)

        is_auth, response, status_code = self.auth_service.is_authorized(
            data, headers, auth_role
        )

        self.assertTrue(is_auth)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, {})
