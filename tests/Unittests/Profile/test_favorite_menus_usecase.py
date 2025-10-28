import unittest
from src.Application.Profiles.ProfileUseCase import ProfileUseCase
from tests.Mocks.Profile.mock_profile_repo import MockProfileRepo


class TestFavoriteMenusUseCase(unittest.TestCase):
    """Unit tests for favorite menus use case"""

    def setUp(self):
        """Setup a mock profile repository and use case for testing"""
        self.mock_repo = MockProfileRepo()
        self.use_case = ProfileUseCase(self.mock_repo)

        # Start with one user profile
        self.mock_repo.create_profile("user1")

    def test_add_favorite_menu_success(self):
        """Test adding a favorite menu successfully"""
        # Add favorite menu
        result = self.use_case.add_favorite_menu("user1", "menu1")

        # Verify addition
        self.assertTrue(result)
        self.assertTrue(self.use_case.is_menu_in_favorites("user1", "menu1"))

    def test_add_duplicate_favorite_menu(self):
        """Test adding a duplicate favorite menu"""
        # Add favorite menu twice
        self.use_case.add_favorite_menu("user1", "menu1")
        result = self.use_case.add_favorite_menu("user1", "menu1")

        # Verify the first addition succeeds
        # while the second one fails due to the duplication
        self.assertFalse(result)

    def test_add_favorite_menu_user_not_found(self):
        """Test adding a favorite menu for a non-existent user"""
        # Add the menu to a profile that doesn't exist
        result = self.use_case.add_favorite_menu("user2", "menu1")

        # Verify it fails since the user doesn't exist
        self.assertFalse(result)

    def test_remove_favorite_menu_success(self):
        """Test removing a favorite menu successfully"""
        # First add a favorite menu
        self.use_case.add_favorite_menu("user1", "menu1")
        # Now remove it
        result = self.use_case.remove_favorite_menu("user1", "menu1")

        # Verify removal
        self.assertTrue(result)
        self.assertFalse(self.use_case.is_menu_in_favorites("user1", "menu1"))

    def test_remove_nonexistent_favorite_menu(self):
        """Test removing a favorite menu that doesn't exist"""
        # Attempt to remove a menu that wasn't added
        result = self.use_case.remove_favorite_menu("user1", "menu2")

        # Verify it fails since the menu isn't in favorites
        self.assertFalse(result)

    def test_remove_favorite_menu_user_not_found(self):
        # Add to a profile that doesn't exist
        result = self.use_case.remove_favorite_menu("user2", "menu1")

        # Verify it fails since the user doesn't exist
        self.assertFalse(result)

    def test_get_favorite_menus(self):
        """Test retrieving favorite menus for a user"""
        # Add some favorite menus
        self.use_case.add_favorite_menu("user1", "menu1")
        self.use_case.add_favorite_menu("user1", "menu2")

        # Retrieve favorite menus
        favorites = self.use_case.get_favorite_menus("user1")

        # Verify the retrieved menus
        self.assertEqual(len(favorites), 2)
        self.assertIn("menu1", favorites)
        self.assertIn("menu2", favorites)
