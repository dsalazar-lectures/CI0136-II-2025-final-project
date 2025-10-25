import unittest
from unittest.mock import patch
from flask import Flask
from src.API.Menu.menuRoutes import recipes_bp
from tests.Mocks.Recipes.mock_recipe_repo import MockRecipe

class MenuEndpointTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(recipes_bp)
        self.client = app.test_client()

    @patch("src.Application.Recipes.recipe_service.get_recipes_by_category")
    def test_get_menu_returns_limited_recipes(self, mock_get_recipes):
        recipes = [
            MockRecipe(1, "recipe1", ["category1", "category2"]),
            MockRecipe(2, "recipe2", ["category1", "category3"]),
            MockRecipe(3, "recipe3", ["category4"])
        ]
        mock_get_recipes.side_effect = lambda category: [r for r in recipes if category in r.categories]
        response = self.client.get("/menu?category=category1")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        names = [r["name"] for r in data]
        self.assertIn("recipe1", names)
        self.assertIn("recipe2", names)

    @patch("src.Application.Recipes.recipe_service.get_recipes_by_category")
    def test_get_menu_empty_category(self, mock_get_recipes):
        mock_get_recipes.return_value = []
        response = self.client.get("/menu?category=unknown")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, [])

    @patch("src.Application.Recipes.recipe_service.get_recipes_by_category")
    def test_get_menu_category_filter(self, mock_get_recipes):
        recipes = [MockRecipe(1, "recipe1", ["category1"]), MockRecipe(2, "recipe2", ["category2"])]
        mock_get_recipes.side_effect = lambda category: [r for r in recipes if category in r.categories]
        response = self.client.get("/menu?category=category2")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "recipe2")

if __name__ == "__main__":
    unittest.main()
