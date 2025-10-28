import unittest
from tests.Mocks.Profile.mock_profile_and_favorite_foods import MockProfileAndFavoriteFoods

class TestProfileAndFavoriteFoods(unittest.TestCase):
    def setUp(self):
        self.repo = MockProfileAndFavoriteFoods()

    def test_create_profile(self):
        # Test creating a new profile
        profile = self.repo.create_profile(1)
        self.assertIsNotNone(profile)
        self.assertEqual(profile.user_id, 1)
        self.assertEqual(profile.favorite_foods, [])
        self.assertEqual(profile.unfavorite_foods, [])
        self.assertEqual(profile.favorite_menus, [])

    def test_get_profile(self):
        # Create a profile
        created_profile = self.repo.create_profile(1)
        self.assertIsNotNone(created_profile)

        # Get the profile
        retrieved_profile = self.repo.get_profile(1)
        self.assertIsNotNone(retrieved_profile)
        self.assertEqual(retrieved_profile.user_id, 1)
        self.assertEqual(retrieved_profile.favorite_foods, [])

    def test_update_favorite_foods(self):
        # Create a profile
        profile = self.repo.create_profile(1)
        self.assertIsNotNone(profile)

        # Update favorite foods
        new_favorites = ["pasta", "pizza"]
        updated_profile = self.repo.update_favorite_foods(1, new_favorites)
        
        self.assertIsNotNone(updated_profile)
        self.assertEqual(updated_profile.favorite_foods, new_favorites)

        # Verify the update persisted
        retrieved_profile = self.repo.get_profile(1)
        self.assertEqual(retrieved_profile.favorite_foods, new_favorites)

    def test_update_nonexistent_profile(self):
        result = self.repo.update_favorite_foods(999, ["pizza"])
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()