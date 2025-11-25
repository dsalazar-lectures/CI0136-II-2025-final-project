import unittest
from unittest.mock import patch, Mock
from flask import Flask
from src.API.Ingredients.IngredientsRoutes import ingredients_bp


class IngredientServiceTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(ingredients_bp)
        self.client = app.test_client()

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_create_ingredient_valid(self, mock_service):
        """Test POST /ingredients/create with valid data"""
        mock_service.create_ingredient.return_value = None

        response = self.client.post(
            "/ingredients/create",
            json={
                "name": "Oat Milk",
                "categories": ["plant_milk"],
                "substitutes": ["almond_milk", "soy_milk"],
                "components": ["oats", "gluten"],
            },
        )

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data["message"], "Ingredient created successfully")
        mock_service.create_ingredient.assert_called_once_with(
            "Oat Milk", ["plant_milk"], ["almond_milk", "soy_milk"], ["oats", "gluten"]
        )

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_create_ingredient_not_valid(self, mock_service):
        """Test POST /ingredients/create without name field"""
        mock_service.create_ingredient.return_value = None

        response = self.client.post(
            "/ingredients/create",
            json={
                "categories": ["plant_milk"],
                "substitutes": ["almond_milk", "soy_milk"],
                "components": ["oats", "gluten"],
            },
        )

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "Ingredient name is required")
        mock_service.create_ingredient.assert_not_called()

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_update_categories(self, mock_service):
        """Test POST /ingredients/update with categories field"""
        mock_ing = Mock()
        mock_service.get_ingredient_by_id.return_value = mock_ing

        response = self.client.post(
            "/ingredients/update", json={"id": 1, "categories": ["dairy", "fat"]}
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Ingredient updated successfully")
        mock_service.update_categories.assert_called_once_with(1, ["dairy", "fat"])

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_update_substitutes(self, mock_service):
        """Test POST /ingredients/update with substitutes field"""
        mock_ing = Mock()
        mock_service.get_ingredient_by_id.return_value = mock_ing

        response = self.client.post(
            "/ingredients/update",
            json={"id": 1, "substitutes": ["Almond Milk", "Oat Milk"]},
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Ingredient updated successfully")
        mock_service.update_substitutes.assert_called_once_with(
            1, ["Almond Milk", "Oat Milk"]
        )

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_update_components(self, mock_service):
        """Test POST /ingredients/update with components field"""
        mock_ing = Mock()
        mock_service.get_ingredient_by_id.return_value = mock_ing

        response = self.client.post(
            "/ingredients/update", json={"id": 1, "components": ["soy", "plant oils"]}
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Ingredient updated successfully")
        mock_service.update_components.assert_called_once_with(1, ["soy", "plant oils"])

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_update_all(self, mock_service):
        """Test POST /ingredients/update with all fields"""
        mock_ing = Mock()
        mock_service.get_ingredient_by_id.return_value = mock_ing

        response = self.client.post(
            "/ingredients/update",
            json={
                "id": 1,
                "categories": ["plant_milk"],
                "substitutes": ["almond_milk", "soy_milk"],
                "components": ["oats", "gluten"],
            },
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Ingredient updated successfully")
        mock_service.update_categories.assert_called_once_with(1, ["plant_milk"])
        mock_service.update_substitutes.assert_called_once_with(
            1, ["almond_milk", "soy_milk"]
        )
        mock_service.update_components.assert_called_once_with(1, ["oats", "gluten"])

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_update_id_not_found(self, mock_service):
        """Test POST /ingredients/update without ID field"""
        mock_service.get_ingredient_by_id.return_value = None

        response = self.client.post(
            "/ingredients/update", json={"id": 999, "categories": ["plant_milk"]}
        )

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["message"], "Ingredient not found")
        mock_service.update_categories.assert_not_called()

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_delete_ingredient_success(self, mock_service):
        """Test POST /ingredients/delete"""
        mock_service.delete_ingredient.return_value = None

        response = self.client.post("/ingredients/delete", json={"id": 1})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Ingredient deleted successfully")
        mock_service.delete_ingredient.assert_called_once()

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_delete_ingredient_id_not_found(self, mock_service):
        """Test POST /ingredients/delete without ID field"""
        mock_service.delete_ingredient.return_value = "ID is not valid"

        response = self.client.post("/ingredients/delete", json={"id": 999})

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "Ingredient not found")
        mock_service.delete_ingredient.assert_called_once()

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_ai_service")
    def test_ai_substitutes_success(self, mock_service):
        """POST /ingredients/ai-substitutes returns 200 and body forwarded"""
        mock_service.get_ai_substitutes_message.return_value = {
            "status_code": 200,
            "body": {
                "ingredient": "Whole Milk",
                "ai_message": ["Oat Milk", "Almond Milk", "Soy Milk"],
            },
        }

        response = self.client.post(
            "/ingredients/ai-substitutes", json={"ingredient": "Whole Milk"}
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("ai_message", data)
        self.assertEqual(data["ai_message"], ["Oat Milk", "Almond Milk", "Soy Milk"])
        mock_service.get_ai_substitutes_message.assert_called_once_with("Whole Milk")

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_ai_service")
    def test_ai_substitutes_missing_ingredient(self, mock_service):
        """POST /ingredients/ai-substitutes without ingredient returns 400"""
        response = self.client.post("/ingredients/ai-substitutes", json={})

        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["error"], "Ingredient name is required")
        mock_service.get_ai_substitutes_message.assert_not_called()


if __name__ == "__main__":
    unittest.main()
