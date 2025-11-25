import unittest
from unittest.mock import Mock
from src.Application.Profiles.Services.ProfileApplicationService import (
    ProfileApplicationService,
)
from src.Model.Profiles.Profiles import Profile
from src.Model.Profiles.Roles import Role


class TestProfileApplicationService(unittest.TestCase):
    """Unit tests for ProfileApplicationService"""

    def setUp(self):
        self.mock_profile_repo = Mock()
        self.profile_service = ProfileApplicationService(self.mock_profile_repo)

    def test_create_profile_success(self):
        # Arrange
        user_id = 1
        expected_profile = Profile(
            user_id=user_id,
            favorite_foods=[],
            unfavorite_foods=[],
            favorite_menus=[],
            role=Role.USER,
        )
        self.mock_profile_repo.create_profile.return_value = expected_profile

        # Act
        result = self.profile_service.create_profile(user_id)

        # Assert
        self.mock_profile_repo.create_profile.assert_called_once_with(user_id)
        self.assertEqual(result, expected_profile)
        self.assertEqual(result.user_id, user_id)

    def test_create_profile_returns_none_on_failure(self):
        # Arrange
        user_id = 1
        self.mock_profile_repo.create_profile.return_value = None

        # Act
        result = self.profile_service.create_profile(user_id)

        # Assert
        self.mock_profile_repo.create_profile.assert_called_once_with(user_id)
        self.assertIsNone(result)

    def test_get_profile_success(self):
        # Arrange
        user_id = 1
        expected_profile = Profile(
            user_id=user_id,
            favorite_foods=[],
            unfavorite_foods=[],
            favorite_menus=[],
            role=Role.USER,
        )
        self.mock_profile_repo.get_profile.return_value = expected_profile

        # Act
        result = self.profile_service.get_profile(user_id)

        # Assert
        self.mock_profile_repo.get_profile.assert_called_once_with(user_id)
        self.assertIsInstance(result, Profile)
        self.assertEqual(result, expected_profile)
        self.assertEqual(result.role, Role.USER)
