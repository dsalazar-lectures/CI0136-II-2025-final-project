# tests/Unittests/Profile/test_profile_model.py
import unittest
from src.Model.Profiles.Profiles import Profile


class TestProfileModel(unittest.TestCase):

    def test_profile_creation_defaults(self):
        profile = Profile(user_id=1)
        self.assertEqual(profile.favorite_foods, [])
        self.assertEqual(profile.unfavorite_foods, [])
        self.assertEqual(profile.favorite_menus, [])
        self.assertEqual(profile.user_id, 1)
