import unittest
from tests.Mocks.Profile.mock_profile_and_favorite_foods import (
    MockProfileAndFavoriteFoods,
)


class TestProfileAndUnfavoriteFoods(unittest.TestCase):
    def setUp(self):
        self.repo = MockProfileAndFavoriteFoods()

    def test_create_profile_unfavorites_empty(self):
        """New profiles should start with empty unfavorite_foods list."""
        profile = self.repo.create_profile(1)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user_id, 1)
        self.assertEqual(profile.unfavorite_foods, [])

    def test_update_unfavorite_foods(self):
        """Updating unfavorite_foods should persist the new list."""
        profile = self.repo.create_profile(1)
        self.assertIsNotNone(profile)

        new_unfavorites = ["mani", "cacao"]
        updated_profile = self.repo.update_unfavorite_foods(1, new_unfavorites)

        self.assertIsNotNone(updated_profile)
        self.assertEqual(updated_profile.unfavorite_foods, new_unfavorites)

        retrieved_profile = self.repo.get_profile(1)
        self.assertIsNotNone(retrieved_profile)
        self.assertEqual(retrieved_profile.unfavorite_foods, new_unfavorites)

    def test_update_unfavorite_foods_nonexistent_profile(self):
        """Updating unfavorites for a non-existent profile should return None."""
        result = self.repo.update_unfavorite_foods(999, ["mani"])
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
