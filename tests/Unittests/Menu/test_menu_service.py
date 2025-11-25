import unittest
from unittest.mock import patch, MagicMock
from src.Application.Menu import menu_service


class MenuServiceTestCase(unittest.TestCase):
    @patch("src.Application.Recipes.recipe_service.get_random_recipe_by_category")
    def test_generate_menus_happy_path(self, mock_get_recipe):
        # Mock recipes for each category
        mock_breakfast = MagicMock()
        mock_breakfast.id = 1
        mock_breakfast.to_dict.return_value = {"id": 1, "name": "Pancakes"}

        mock_lunch = MagicMock()
        mock_lunch.id = 2
        mock_lunch.to_dict.return_value = {"id": 2, "name": "Pasta"}

        mock_dinner = MagicMock()
        mock_dinner.id = 3
        mock_dinner.to_dict.return_value = {"id": 3, "name": "Salmón"}

        mock_dessert = MagicMock()
        mock_dessert.id = 4
        mock_dessert.to_dict.return_value = {"id": 4, "name": "Flan"}

        # Configure mock to return appropriate recipe based on category
        def get_recipe_by_category(category):
            if category == "desayuno":
                return mock_breakfast
            elif category == "almuerzo":
                return mock_lunch
            elif category == "cena":
                return mock_dinner
            elif category == "postre":
                return mock_dessert
            return None

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
        mock_recipe = MagicMock()
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
            mock_recipe = MagicMock()
            mock_recipe.id = 1
            mock_recipe.to_dict.return_value = {"id": 1, "name": "Recipe"}
            return mock_recipe

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
