# tests/Unittests/Profile/test_profile_repository.py
import unittest
import os
import tempfile
import unittest.mock
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository
from src.Model.Profiles.Profiles import Profile


class TestProfileRepository(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix="_test_profiles.csv"
        )
        self.temp_file.close()

        # Write header to the themp CSV file
        with open(self.temp_file.name, "w", newline="") as f:
            f.write("user_id,favorite_foods,unfavorite_foods,favorite_menus\n")

        self.profile_repo = ProfileRepository(self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_create_profile_success(self):
        # Act
        result = self.profile_repo.create_profile(1)

        # Assert
        self.assertIsInstance(result, Profile)
        self.assertEqual(result.user_id, 1)
        self.assertEqual(result.favorite_foods, [])
        self.assertEqual(result.unfavorite_foods, [])
        self.assertEqual(result.favorite_menus, [])

    def test_create_profile_multiple_users(self):
        # Act
        profile1 = self.profile_repo.create_profile(1)
        profile2 = self.profile_repo.create_profile(2)

        # Assert
        self.assertEqual(profile1.user_id, 1)
        self.assertEqual(profile2.user_id, 2)

    def test_create_profile_returns_none_on_failure(self):
        # Simulate database failure by mocking the database method to return None
        with unittest.mock.patch.object(
            self.profile_repo.profile_database, "create_profile", return_value=None
        ):
            result = self.profile_repo.create_profile(1)
            self.assertIsNone(result)
