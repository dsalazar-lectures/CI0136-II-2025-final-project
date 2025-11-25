import unittest
from unittest.mock import Mock, patch
import jwt
from src.Application.User.Services.AccountApplicationService import (
    AccountApplicationService,
)


class TestAccountApplicationService(unittest.TestCase):

    def setUp(self):
        # Create mocks for dependencies
        self.mock_user_repository = Mock()
        self.mock_profile_repository = Mock()
        self.mock_token_service = Mock()

        # Initialize service with mocks
        self.account_service = AccountApplicationService(
            user_repository=self.mock_user_repository,
            profile_repository=self.mock_profile_repository,
            token_service=self.mock_token_service,
        )

    def test_delete_user_account_success(self):
        """Test successful account deletion"""
        # Arrange
        headers = {"Authorization": "Bearer valid_token"}
        username_to_delete = "userToDelete"

        # Mock authenticated user
        authenticated_user = Mock()
        authenticated_user.username = "authenticatedUser"

        # Mock user to delete
        user_to_delete = Mock()
        user_to_delete.id = 123
        user_to_delete.username = username_to_delete

        # Mock profile to delete
        mock_profile = Mock()
        mock_profile.favorite_foods = ["pizza", "pasta"]

        # Mock token validation
        with patch("jwt.decode") as mock_jwt_decode:
            mock_jwt_decode.return_value = {"username": "authenticatedUser"}

            # Mock session verification
            self.mock_user_repository.get_user_by_username.side_effect = [
                authenticated_user,
                user_to_delete,
            ]
            self.mock_token_service.verify_token.return_value = True

            # Mock successful deletions
            self.mock_profile_repository.get_profile.return_value = mock_profile
            self.mock_profile_repository.delete_profile.return_value = True
            self.mock_user_repository.delete_user.return_value = True

            # Act
            result_user, response, status_code = (
                self.account_service.delete_user_account(headers, username_to_delete)
            )

            # Assert
            self.assertEqual(result_user, user_to_delete)
            self.assertEqual(
                response["message"], "User account and profile deleted successfully"
            )
            self.assertEqual(status_code, 200)

            # Verify method calls
            self.mock_profile_repository.get_profile.assert_called_once_with(123)
            self.mock_profile_repository.delete_profile.assert_called_once_with(123)
            self.mock_user_repository.delete_user.assert_called_once_with(123)
            # Verify restore_profile was NOT called (success case)
            self.mock_profile_repository.restore_profile.assert_not_called()

    def test_delete_user_account_missing_authorization_header(self):
        """Test deletion with missing Authorization header"""
        # Arrange
        headers = {}
        username_to_delete = "userToDelete"

        # Act
        result_user, response, status_code = self.account_service.delete_user_account(
            headers, username_to_delete
        )

        # Assert
        self.assertIsNone(result_user)
        self.assertEqual(response["error"], "Missing or invalid Authorization header")
        self.assertEqual(status_code, 401)

    def test_delete_user_account_invalid_token_format(self):
        """Test deletion with invalid token format"""
        # Arrange
        headers = {"Authorization": "InvalidFormat"}
        username_to_delete = "userToDelete"

        # Act
        result_user, response, status_code = self.account_service.delete_user_account(
            headers, username_to_delete
        )

        # Assert
        self.assertIsNone(result_user)
        self.assertEqual(response["error"], "Missing or invalid Authorization header")
        self.assertEqual(status_code, 401)

    def test_delete_user_account_invalid_token(self):
        """Test deletion with invalid JWT token"""
        # Arrange
        headers = {"Authorization": "Bearer invalid_token"}
        username_to_delete = "userToDelete"

        # Mock invalid token
        with patch("jwt.decode") as mock_jwt_decode:
            mock_jwt_decode.side_effect = jwt.InvalidTokenError("Invalid token")

            # Act
            result_user, response, status_code = (
                self.account_service.delete_user_account(headers, username_to_delete)
            )

            # Assert
            self.assertIsNone(result_user)
            self.assertEqual(response["error"], "Invalid token")
            self.assertEqual(status_code, 401)

    def test_delete_user_account_invalid_token_payload(self):
        """Test deletion with token missing username"""
        # Arrange
        headers = {"Authorization": "Bearer valid_token"}
        username_to_delete = "userToDelete"

        # Mock token without username
        with patch("jwt.decode") as mock_jwt_decode:
            mock_jwt_decode.return_value = {"other_field": "value"}

            # Act
            result_user, response, status_code = (
                self.account_service.delete_user_account(headers, username_to_delete)
            )

            # Assert
            self.assertIsNone(result_user)
            self.assertEqual(response["error"], "Invalid token payload")
            self.assertEqual(status_code, 401)

    def test_delete_user_account_expired_session(self):
        """Test deletion with expired session"""
        # Arrange
        headers = {"Authorization": "Bearer valid_token"}
        username_to_delete = "userToDelete"

        # Mock token validation
        with patch("jwt.decode") as mock_jwt_decode:
            mock_jwt_decode.return_value = {"username": "authenticatedUser"}

            # Mock session verification failure
            self.mock_user_repository.get_user_by_username.return_value = Mock()
            self.mock_token_service.verify_token.return_value = False

            # Act
            result_user, response, status_code = (
                self.account_service.delete_user_account(headers, username_to_delete)
            )

            # Assert
            self.assertIsNone(result_user)
            self.assertEqual(response["error"], "Expired session")
            self.assertEqual(status_code, 401)

    def test_delete_user_account_user_not_found(self):
        """Test deletion when user to delete doesn't exist"""
        # Arrange
        headers = {"Authorization": "Bearer valid_token"}
        username_to_delete = "nonExistentUser"

        # Mock token validation
        with patch("jwt.decode") as mock_jwt_decode:
            mock_jwt_decode.return_value = {"username": "authenticatedUser"}

            # Mock session verification success
            authenticated_user = Mock()
            self.mock_user_repository.get_user_by_username.side_effect = [
                authenticated_user,
                None,  # Second call for user to delete (not found)
            ]
            self.mock_token_service.verify_token.return_value = True

            # Act
            result_user, response, status_code = (
                self.account_service.delete_user_account(headers, username_to_delete)
            )

            # Assert
            self.assertIsNone(result_user)
            self.assertEqual(response["error"], "User not found")
            self.assertEqual(status_code, 404)

    def test_delete_user_account_profile_not_found(self):
        """Test when user profile is not found"""
        # Arrange
        headers = {"Authorization": "Bearer valid_token"}
        username_to_delete = "userToDelete"

        # Mock authenticated user and user to delete
        authenticated_user = Mock()
        user_to_delete = Mock()
        user_to_delete.id = 123

        # Mock token validation
        with patch("jwt.decode") as mock_jwt_decode:
            mock_jwt_decode.return_value = {"username": "authenticatedUser"}

            self.mock_user_repository.get_user_by_username.side_effect = [
                authenticated_user,
                user_to_delete,
            ]
            self.mock_token_service.verify_token.return_value = True

            # Mock profile not found
            self.mock_profile_repository.get_profile.return_value = None

            # Act
            result_user, response, status_code = (
                self.account_service.delete_user_account(headers, username_to_delete)
            )

            # Assert
            self.assertIsNone(result_user)
            self.assertEqual(response["error"], "User profile not found")
            self.assertEqual(status_code, 404)

    def test_delete_user_account_profile_deletion_fails(self):
        """Test when profile deletion fails - user should NOT be deleted"""
        # Arrange
        headers = {"Authorization": "Bearer valid_token"}
        username_to_delete = "userToDelete"

        # Mock authenticated user and user to delete
        authenticated_user = Mock()
        user_to_delete = Mock()
        user_to_delete.id = 123

        # Mock profile to delete
        mock_profile = Mock()
        mock_profile.favorite_foods = ["pizza", "pasta"]

        # Mock token validation
        with patch("jwt.decode") as mock_jwt_decode:
            mock_jwt_decode.return_value = {"username": "authenticatedUser"}

            self.mock_user_repository.get_user_by_username.side_effect = [
                authenticated_user,
                user_to_delete,
            ]
            self.mock_token_service.verify_token.return_value = True

            # Mock profile deletion failure
            self.mock_profile_repository.get_profile.return_value = mock_profile
            self.mock_profile_repository.delete_profile.return_value = False

            # Act
            result_user, response, status_code = (
                self.account_service.delete_user_account(headers, username_to_delete)
            )

            # Assert
            self.assertIsNone(result_user)
            self.assertEqual(response["error"], "Failed to delete user profile")
            self.assertEqual(status_code, 500)

            # Verify user deletion was NOT attempted when profile deletion fails
            self.mock_user_repository.delete_user.assert_not_called()
            # Verify restore_profile was NOT called (only for user deletion failure)
            self.mock_profile_repository.restore_profile.assert_not_called()

    def test_delete_user_account_user_deletion_fails_with_rollback(self):
        """Test when user account deletion fails - profile should be restored"""
        # Arrange
        headers = {"Authorization": "Bearer valid_token"}
        username_to_delete = "userToDelete"

        # Mock authenticated user and user to delete
        authenticated_user = Mock()
        user_to_delete = Mock()
        user_to_delete.id = 123

        # Mock profile to delete
        mock_profile = Mock()
        mock_profile.favorite_foods = ["pizza", "pasta"]

        # Mock token validation
        with patch("jwt.decode") as mock_jwt_decode:
            mock_jwt_decode.return_value = {"username": "authenticatedUser"}

            self.mock_user_repository.get_user_by_username.side_effect = [
                authenticated_user,
                user_to_delete,
            ]
            self.mock_token_service.verify_token.return_value = True

            # Mock profile deletion success but user deletion failure
            self.mock_profile_repository.get_profile.return_value = mock_profile
            self.mock_profile_repository.delete_profile.return_value = True
            self.mock_user_repository.delete_user.return_value = False

            # Act
            result_user, response, status_code = (
                self.account_service.delete_user_account(headers, username_to_delete)
            )

            # Assert
            self.assertIsNone(result_user)
            self.assertEqual(response["error"], "Failed to delete user account")
            self.assertEqual(status_code, 500)

            # Verify rollback was attempted
            self.mock_profile_repository.restore_profile.assert_called_once_with(
                123, mock_profile.favorite_foods
            )

    def test_delete_user_account_authenticated_user_not_found(self):
        """Test when authenticated user is not found in database"""
        # Arrange
        headers = {"Authorization": "Bearer valid_token"}
        username_to_delete = "userToDelete"

        # Mock token validation
        with patch("jwt.decode") as mock_jwt_decode:
            mock_jwt_decode.return_value = {"username": "authenticatedUser"}

            # Mock user not found for authenticated user
            self.mock_user_repository.get_user_by_username.return_value = None

            # Act
            result_user, response, status_code = (
                self.account_service.delete_user_account(headers, username_to_delete)
            )

            # Assert
            self.assertIsNone(result_user)
            self.assertEqual(response["error"], "User not found")
            self.assertEqual(status_code, 404)


if __name__ == "__main__":
    unittest.main()
