import unittest
from unittest.mock import patch
from src.Application.Menu import menu_service
from tests.Mocks.Recipes.mock_recipe_repo import MockRecipe


class MenuServiceTestCase(unittest.TestCase):
    def _create_mock_recipe(self, recipe_id, name, category):
        """Helper to create a mock recipe"""
        return MockRecipe(recipe_id, name, [category])

    @patch("src.Application.Recipes.recipe_service.get_random_recipe_by_category")
    def test_generate_menus_happy_path(self, mock_get_recipe):
        # Create mock recipes using helper
        mock_breakfast = self._create_mock_recipe(1, "Pancakes", "desayuno")
        mock_lunch = self._create_mock_recipe(2, "Pasta", "almuerzo")
        mock_dinner = self._create_mock_recipe(3, "Salmón", "cena")
        mock_dessert = self._create_mock_recipe(4, "Flan", "postre")

        # Configure mock to return appropriate recipe based on category
        def get_recipe_by_category(category):
            recipes = {
                "desayuno": mock_breakfast,
                "almuerzo": mock_lunch,
                "cena": mock_dinner,
                "postre": mock_dessert,
            }
            return recipes.get(category)

        mock_get_recipe.side_effect = get_recipe_by_category

        menu, missing_categories, menu_details = menu_service.generate_menus(2)

        # Verify no missing categories
        self.assertIsNone(missing_categories)

        # Verify menu object
        self.assertIsNotNone(menu)
        self.assertEqual(len(menu.daily_menus), 2)

        # Verify menu details
        self.assertEqual(len(menu_details), 2)
        self.assertEqual(menu_details[0]["day"], 1)
        self.assertEqual(menu_details[0]["breakfast"]["name"], "Pancakes")
        self.assertEqual(menu_details[0]["lunch"]["name"], "Pasta")
        self.assertEqual(menu_details[0]["dinner"]["name"], "Salmón")
        self.assertEqual(menu_details[0]["dessert"]["name"], "Flan")

    @patch("src.Application.Recipes.recipe_service.get_random_recipe_by_category")
    def test_empty_recipes_returns_missing_categories(self, mock_get_recipe):
        # Mock that no recipes are found for any category
        mock_get_recipe.return_value = None

        menu, missing_categories, menu_details = menu_service.generate_menus(1)

        # Verify all categories are missing
        self.assertIsNone(menu)
        self.assertIsNone(menu_details)
        self.assertIsNotNone(missing_categories)
        self.assertIn("desayuno", missing_categories)
        self.assertIn("almuerzo", missing_categories)
        self.assertIn("cena", missing_categories)
        self.assertIn("postre", missing_categories)

    @patch("src.Application.Recipes.recipe_service.get_random_recipe_by_category")
    def test_count_zero_returns_empty(self, mock_get_recipe):
        # Even with available recipes, count 0 should return empty menu
        mock_recipe = self._create_mock_recipe(1, "Recipe", "desayuno")
        mock_get_recipe.return_value = mock_recipe

        menu, missing_categories, menu_details = menu_service.generate_menus(0)

        # Verify empty results
        self.assertIsNotNone(menu)
        self.assertEqual(len(menu.daily_menus), 0)
        self.assertEqual(len(menu_details), 0)

    def test_non_int_count_raises(self):
        with self.assertRaises(TypeError):
            # passing a string should raise when used in range()
            menu_service.generate_menus("3")

    @patch("src.Application.Recipes.recipe_service.get_random_recipe_by_category")
    def test_missing_one_category(self, mock_get_recipe):
        # Mock that only breakfast is missing
        def get_recipe_by_category(category):
            if category == "desayuno":
                return None
            return self._create_mock_recipe(1, "Recipe", category)

        mock_get_recipe.side_effect = get_recipe_by_category

        menu, missing_categories, menu_details = menu_service.generate_menus(1)

        # Verify only breakfast is missing
        self.assertIsNone(menu)
        self.assertIsNone(menu_details)
        self.assertIsNotNone(missing_categories)
        self.assertIn("desayuno", missing_categories)
        self.assertEqual(len(missing_categories), 1)


if __name__ == "__main__":
    unittest.main()
