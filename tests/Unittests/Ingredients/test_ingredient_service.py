import unittest
from unittest.mock import patch
from types import SimpleNamespace
from flask import Flask
from src.API.Ingredients.IngredientsRoutes import ingredients_bp
from tests.Mocks.mock_ingredients import MockIngredient
from tests.Mocks.mock_ingredients import (
    INGREDIENT_1,
    INGREDIENT_2,
    INGREDIENT_3,
    SIMPLE_INGREDIENT_1,
    SIMPLE_INGREDIENT_2,
    SIMPLE_INGREDIENT_3,
)

class IngredientServiceTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(ingredients_bp,  url_prefix="/api")
        self.client = app.test_client()

    # --- GET simplified ingredients ---
    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_get_all_ingredients_simplified(self, mock_service):
        mock_service.get_all_ingredients.return_value = [
            SimpleNamespace(**SIMPLE_INGREDIENT_1),
            SimpleNamespace(**SIMPLE_INGREDIENT_2),
            SimpleNamespace(**SIMPLE_INGREDIENT_3),
        ]

        response = self.client.get("/api/ingredients?simple=true")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
        self.assertEqual(response.json[0]["name"], SIMPLE_INGREDIENT_1["name"])

    # --- Search ingredients by name ---
    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_search_ingredients_by_name(self, mock_service):
        mock_service.get_ingredient_by_name.side_effect = lambda name: INGREDIENT_1 if name == "Onion" else INGREDIENT_2

        response = self.client.post(
            "/api/ingredients/search",
            json={"names": ["Onion", "Milk"]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["results"]), 2)
        self.assertEqual(response.json["results"][0]["name"], INGREDIENT_1.name)

    # --- Search ingredients simplified ---
    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_search_ingredients_simplified(self, mock_service):
        mock_service.get_ingredient_by_name.side_effect = lambda name: MockIngredient(
            id=1 if name == "Salt" else 2, name=name
        )

        response = self.client.post(
            "/api/ingredients/search?simple=true",
            json={"names": ["Salt", "Milk"]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json["results"]), 2)
        self.assertEqual(response.json["results"][0]["name"], "Salt")
        self.assertEqual(response.json["results"][1]["name"], "Milk")

    # --- Create ingredient ---
    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_create_ingredient_valid(self, mock_service):
        mock_service.create_ingredient.return_value = INGREDIENT_3.to_json()

        response = self.client.post(
            "/api/ingredients/create",
            json={
            "name": "Cheese",
            "categories": ["Dairy"],
            "substitutes": [],
            "components": ["Milk", "Fat"],
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json["message"], "Ingredient created successfully")


    # --- Update categories ---
    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_update_categories(self, mock_service):
        mock_service.get_ingredient_by_id.return_value = INGREDIENT_1
        mock_service.update_categories.return_value = INGREDIENT_1.to_json()

        response = self.client.post(
            "/api/ingredients/update",
            json={"id": 1, "categories": ["spice", "fresh"]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Ingredient updated successfully")

    # --- Delete ingredient ---
    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_delete_ingredient(self, mock_service):
        mock_service.get_ingredient_by_id.return_value = INGREDIENT_2
        mock_service.delete_ingredient.return_value = True

        response = self.client.post(
        "/api/ingredients/delete",
        json={"id": 2},
    )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Ingredient deleted successfully")


if __name__ == "__main__":
    unittest.main()
