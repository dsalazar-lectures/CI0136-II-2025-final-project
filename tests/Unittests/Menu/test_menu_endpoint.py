import unittest
from unittest.mock import patch
from flask import Flask
from src.Application.Menu import MenuUseCase
from src.API.Menu.menuRoutes import create_menu_blueprints
from tests.Mocks.Recipes.mock_recipe import MockRecipe


class MenuEndpointTestCase(unittest.TestCase):
    def setUp(self):
        menu_bp, _ = create_menu_blueprints("test_profiles.csv")
        app = Flask(__name__)
        app.register_blueprint(menu_bp, url_prefix="/api")
        self.client = app.test_client()

    @patch("src.Application.Recipes.recipe_service.get_random_recipe_by_categories")
    def test_get_menu_returns_empty_when_no_recipes(self, mock_get_random_recipe):
        mock_get_random_recipe.return_value = None
        response = self.client.get("/api/menu")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        expected_keys = sorted(["breakfast", "lunch", "dinner", "dessert"])
        self.assertEqual(list(data.keys()), expected_keys)
        for meal in expected_keys:
            self.assertEqual(data[meal], {})

    @patch(
        "src.Infrastructure.Recipes.CSVRecipeRepository.CSVRecipeRepository.find_by_categories"
    )
    def test_get_menu_returns_recipes(self, find_by_categories_mock):
        recipes = [
            MockRecipe(1, "breakfast_recipe", ["breakfast"]),
            MockRecipe(1, "lunch_recipe", ["lunch"]),
            MockRecipe(1, "dinner_recipe", ["dinner"]),
            MockRecipe(1, "dessert_recipe", ["dessert"]),
        ]

        def side_effect(categories):
            for recipe in recipes:
                if any(cat in recipe.categories for cat in categories):
                    return [recipe]
            return []

        find_by_categories_mock.side_effect = side_effect
        response = self.client.get("/api/menu")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        expected_keys = sorted(["breakfast", "lunch", "dinner", "dessert"])
        self.assertEqual(list(data.keys()), expected_keys)
        for meal in expected_keys:
            self.assertIsInstance(data[meal], dict)
            self.assertIn("name", data[meal])
            self.assertEqual(data[meal]["name"], f"{meal}_recipe")

    def test_get_menu_emailPdf_invalid_address(self):
        response = MenuUseCase.emailPdf(1, "test.gmail.com")
        self.assertEqual(response, 400)


if __name__ == "__main__":
    unittest.main()
