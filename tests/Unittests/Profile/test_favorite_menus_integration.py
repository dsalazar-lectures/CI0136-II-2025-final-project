import unittest
import os
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository


class TestFavoriteMenusIntegration(unittest.TestCase):
    """Integration tests for favorite menus functionality with the real repo"""

    def setUp(self):
        """Setup real profile repository"""
        self.test_csv = "test_profiles.csv"
        self.repo = ProfileRepository(self.test_csv)

        # Create test profiles
        self.repo.create_profile(user_id=1)
        self.repo.create_profile(user_id=2)

    def tearDown(self):
        # Clean up test CSV file
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)

    def test_add_and_retrieve_favorite_menu(self):
        """Test adding and retrieving a favorite menu"""
        # Add favorite menu
        result = self.repo.add_favorite_menu(1, "menu1")
        self.assertTrue(result)

        # Check if it's in favorites
        # Use the is_menu_in_favorites method
        self.assertTrue(self.repo.is_menu_in_favorites(1, "menu1"))

    def test_remove_favorite_menu(self):
        """Test removing a favorite menu"""
        # Add favorite menu first
        self.repo.add_favorite_menu(1, "menu1")

        # Now remove it
        result = self.repo.remove_favorite_menu(1, "menu1")

        # Verify removal
        self.assertTrue(result)
        self.assertFalse(self.repo.is_menu_in_favorites(1, "menu1"))

    def test_persistence_across_repository_instances(self):
        """Test data persistence across different repository instances"""
        # Add favorite menu with first repo instance
        self.repo.add_favorite_menu(1, "menu1")
        self.repo.add_favorite_menu(1, "menu2")
        self.repo.add_favorite_menu(2, "menu3")

        # Create a new repo, with the same CSV
        new_repo = ProfileRepository(self.test_csv)

        # Verify data persisted
        user1_favorites = new_repo.get_favorite_menus(1)
        user2_favorites = new_repo.get_favorite_menus(2)

        # User 1
        self.assertEqual(len(user1_favorites), 2)
        self.assertIn("menu1", user1_favorites)
        self.assertIn("menu2", user1_favorites)

        # User 2
        self.assertEqual(len(user2_favorites), 1)
        self.assertIn("menu3", user2_favorites)

    def test_multiple_users_favorite_menus_isolation(self):
        """Test that CSV correctly stores and isolates multiple user profiles"""
        # Add different favorites for different users
        self.repo.add_favorite_menu(1, "menu1")
        self.repo.add_favorite_menu(1, "menu2")
        self.repo.add_favorite_menu(2, "menu3")
        self.repo.add_favorite_menu(2, "menu4")

        # Verify isolation
        user1_favorites = self.repo.get_favorite_menus(1)
        user2_favorites = self.repo.get_favorite_menus(2)

        # Verify length
        self.assertEqual(len(user1_favorites), 2)
        self.assertEqual(len(user2_favorites), 2)

        # Verify no cross-contamination
        self.assertNotIn("menu3", user1_favorites)
        self.assertNotIn("menu4", user1_favorites)
        self.assertNotIn("menu1", user2_favorites)
        self.assertNotIn("menu2", user2_favorites)

    def test_large_number_of_favorites(self):
        """Test handling a large number of favorite menus"""
        # Add 50 favorite menus
        for i in range(50):
            result = self.repo.add_favorite_menu(1, f"menu{i}")
            self.assertTrue(result)

        # Verify all were added
        favorites = self.repo.get_favorite_menus(1)
        self.assertEqual(len(favorites), 50)

        # Verify persistence
        new_repo = ProfileRepository(self.test_csv)
        favorites_reloaded = new_repo.get_favorite_menus(1)
        self.assertEqual(len(favorites_reloaded), 50)

        # Verify a few random ones
        self.assertIn("menu0", favorites_reloaded)
        self.assertIn("menu25", favorites_reloaded)
        self.assertIn("menu49", favorites_reloaded)

    def test_favorite_menu_functions_no_user_error(self):
        """Test favorite menu functions handle non-existent users gracefully"""
        # Non-existent user
        result = self.repo.add_favorite_menu(999, "menuX")
        self.assertFalse(result)

        result = self.repo.remove_favorite_menu(999, "menuX")
        self.assertFalse(result)

        result = self.repo.get_favorite_menus(999)
        self.assertEqual(result, [])

    def test_empty_favorite_menus(self):
        """Test retrieving favorite menus when none have been added"""
        favorites = self.repo.get_favorite_menus(1)
        self.assertEqual(favorites, [])  # Should be empty list
