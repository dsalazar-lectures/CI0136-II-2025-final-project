import unittest
from unittest.mock import patch
from flask import Flask
from src.Application.Menu import MenuUseCase
from src.API.Menu.menuRoutes import menu_bp
from tests.Mocks.Recipes.mock_recipe_repo import MockRecipe


class MenuEndpointTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(menu_bp, url_prefix="/api")
        self.client = app.test_client()

    @patch("src.Application.Recipes.recipe_service.get_recipes_by_category")
    def test_get_menu_returns_empty_list_when_recipes_repo_empty(self, mock_get_recipes):
        mock_get_recipes.return_value = []
        response = self.client.get("/api/menu?category=unknown")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, [{}])

    @patch("src.Application.Recipes.recipe_service.get_recipes_by_category")
    def test_get_menu_category_filter(self, mock_get_recipes):
        recipes = [
            MockRecipe(1, "recipe1", ["category1"]),
            MockRecipe(2, "recipe2", ["category2"]),
        ]
        mock_get_recipes.side_effect = lambda category: [
            r for r in recipes if category in r.categories
        ]
        response = self.client.get("/api/menu?category=category2")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "recipe2")

    @patch("src.Application.Recipes.recipe_service.get_random_recipe_by_category")
    def test_get_menu_returns_one_random_recipe(self, mock_get_random_recipe):
        recipe = MockRecipe(1, "recipe1", ["category1", "category2"])
        mock_get_random_recipe.return_value = recipe
        response = self.client.get("/api/menu?category=category1")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "recipe1")

    @patch("src.Application.Recipes.recipe_service.get_random_recipe_by_category")
    def test_get_menu_empty_category(self, mock_get_random_recipe):
        mock_get_random_recipe.return_value = None
        response = self.client.get("/api/menu?category=unknown")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, [{}])

    @patch("src.Application.Recipes.recipe_service.get_random_recipe_by_category")
    def test_get_menu_category_filter(self, mock_get_random_recipe):
        recipe = MockRecipe(2, "recipe2", ["category2"])
        mock_get_random_recipe.return_value = recipe
        response = self.client.get("/api/menu?category=category2")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "recipe2")

    def test_get_menu_emailPdf_invalid_address(self):
        response = MenuUseCase.emailPdf(1, "test.gmail.com")
        self.assertEqual(response, 400)


if __name__ == "__main__":
    unittest.main()
