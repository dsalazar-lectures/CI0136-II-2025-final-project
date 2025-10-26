import unittest
from unittest.mock import patch
from flask import Flask
from src.API.Menu.menuRoutes import recipes_bp
from tests.Mocks.Recipes.mock_recipe_repo import MockRecipe


class GenerateMenusTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(recipes_bp)
        self.client = app.test_client()

    @patch("src.Application.Recipes.recipe_service.get_recipes_by_category")
    def test_generate_menus_query_count(self, mock_get_recipes):
        recipes = [
            MockRecipe(1, "recipe1", ["category1"]),
            MockRecipe(2, "recipe2", ["category1"]),
        ]
        mock_get_recipes.return_value = recipes

        response = self.client.get("/menu/category1/2")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["menu"], "Menú #1")
        self.assertEqual(data[1]["menu"], "Menú #2")
        names = [m["recipe"]["name"] for m in data]
        self.assertEqual(names, ["recipe1", "recipe2"])

    @patch("src.Application.Recipes.recipe_service.get_recipes_by_category")
    def test_generate_menus_path_repeats_when_count_exceeds(self, mock_get_recipes):
        recipes = [
            MockRecipe(1, "recipe1", ["categoryA"]),
            MockRecipe(2, "recipe2", ["categoryA"]),
        ]
        mock_get_recipes.return_value = recipes

        # Request 3 menus but only 2 recipes exist -> expect repetition (r1, r2, r1)
        response = self.client.get("/menu/categoryA/3")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 3)
        names = [m["recipe"]["name"] for m in data]
        self.assertEqual(names, ["recipe1", "recipe2", "recipe1"])


if __name__ == "__main__":
    unittest.main()
