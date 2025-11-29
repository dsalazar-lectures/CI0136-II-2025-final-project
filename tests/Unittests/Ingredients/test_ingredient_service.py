import unittest
from unittest.mock import patch, Mock
from flask import Flask
from src.API.Ingredients.IngredientsRoutes import ingredients_bp


class IngredientServiceTestCase(unittest.TestCase):
    def setUp(self):

        app = Flask(__name__)

        app.register_blueprint(ingredients_bp, url_prefix="/api")
        self.client = app.test_client()

        self.API_PREFIX = "/api/ingredients"

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_create_ingredient_valid(self, mock_service):
        """Test POST /api/ingredients/create with valid data"""
        mock_service.create_ingredient.return_value = None

        response = self.client.post(
            f"{self.API_PREFIX}/create",
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
        """Test POST /api/ingredients/create without name field"""
        mock_service.create_ingredient.return_value = None

        response = self.client.post(
            f"{self.API_PREFIX}/create",
            json={
                "categories": ["plant_milk"],
                "substitutes": ["almond_milk", "soy_milk"],
                "components": ["oats", "gluten"],
            },
        )

        self.assertEqual(response.status_code, 400)

        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data.get("error"), "Ingredient name is required")
        mock_service.create_ingredient.assert_not_called()

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_update_categories(self, mock_service):
        """Test POST /api/ingredients/update with categories field"""
        mock_ing = Mock()
        mock_service.get_ingredient_by_id.return_value = mock_ing

        response = self.client.post(
            f"{self.API_PREFIX}/update", json={"id": 1, "categories": ["dairy", "fat"]}
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Ingredient updated successfully")
        mock_service.update_categories.assert_called_once_with(1, ["dairy", "fat"])

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_update_substitutes(self, mock_service):
        """Test POST /api/ingredients/update with substitutes field"""
        mock_ing = Mock()
        mock_service.get_ingredient_by_id.return_value = mock_ing

        response = self.client.post(
            f"{self.API_PREFIX}/update",
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
        """Test POST /api/ingredients/update with components field"""
        mock_ing = Mock()
        mock_service.get_ingredient_by_id.return_value = mock_ing

        response = self.client.post(
            f"{self.API_PREFIX}/update",
            json={"id": 1, "components": ["soy", "plant oils"]},
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Ingredient updated successfully")
        mock_service.update_components.assert_called_once_with(1, ["soy", "plant oils"])

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_update_all(self, mock_service):
        """Test POST /api/ingredients/update with all fields"""
        mock_ing = Mock()
        mock_service.get_ingredient_by_id.return_value = mock_ing

        response = self.client.post(
            f"{self.API_PREFIX}/update",
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
        """Test POST /api/ingredients/update when ID is not found"""
        mock_service.get_ingredient_by_id.return_value = None

        response = self.client.post(
            f"{self.API_PREFIX}/update", json={"id": 999, "categories": ["plant_milk"]}
        )

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["message"], "Ingredient not found")
        mock_service.update_categories.assert_not_called()

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_delete_ingredient_success(self, mock_service):
        """Test POST /api/ingredients/delete"""
        mock_service.delete_ingredient.return_value = None

        response = self.client.post(f"{self.API_PREFIX}/delete", json={"id": 1})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Ingredient deleted successfully")
        mock_service.delete_ingredient.assert_called_once_with(1)

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_delete_ingredient_id_not_found(self, mock_service):
        """Test POST /api/ingredients/delete when ID is not found"""
        mock_service.delete_ingredient.return_value = "ID is not valid"

        response = self.client.post(f"{self.API_PREFIX}/delete", json={"id": 999})

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data.get("error"), "Ingredient not found")
        mock_service.delete_ingredient.assert_called_once_with(999)

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_search_by_multiple_names_returns_results_and_not_found(self, mock_service):
        # setup: "tomate" exists, "cebolla" does not
        tomate = Mock()
        tomate.id = 1
        tomate.name = "tomate"
        tomate.to_json.return_value = {"id": 1, "name": "tomate"}

        def get_by_name_side(name):
            return tomate if name.lower() == "tomate" else None

        mock_service.get_ingredient_by_name.side_effect = get_by_name_side

        resp = self.client.post(
            "/ingredients/search", json={"names": ["tomate", "cebolla"]}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("results", data)
        self.assertIn("not_found", data)
        self.assertTrue(any(item["id"] == 1 for item in data["results"]))
        self.assertIn("cebolla", data["not_found"])

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_search_single_name_not_found_returns_404(self, mock_service):
        mock_service.get_ingredient_by_name.return_value = None
        resp = self.client.post("/ingredients/search", json={"names": "noexist"})
        self.assertEqual(resp.status_code, 404)
        data = resp.get_json()
        self.assertIn("error", data)

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_search_by_ids_returns_results_and_not_found(self, mock_service):
        # id 1 exists, id 2 does not
        ingr1 = Mock()
        ingr1.id = 1
        ingr1.name = "A"
        ingr1.to_json.return_value = {"id": 1, "name": "A"}

        def get_by_id_side(i):
            return ingr1 if i == 1 else None

        mock_service.get_ingredient_by_id.side_effect = get_by_id_side

        resp = self.client.post("/ingredients/search", json={"ids": [1, 2]})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("results", data)
        self.assertIn("not_found", data)
        self.assertTrue(any(item["id"] == 1 for item in data["results"]))
        self.assertIn(2, data["not_found"])

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_search_by_categories_returns_matching_ingredients(self, mock_service):
        milk = Mock()
        milk.id = 10
        milk.name = "Whole Milk"
        milk.to_json.return_value = {"id": 10, "name": "Whole Milk"}

        butter = Mock()
        butter.id = 11
        butter.name = "Butter"
        butter.to_json.return_value = {"id": 11, "name": "Butter"}

        mock_service.get_ingredients_by_category.return_value = [milk, butter]

        resp = self.client.post("/ingredients/search", json={"categories": ["dairy"]})
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("results", data)
        ids = {r["id"] for r in data["results"]}
        self.assertIn(10, ids)
        self.assertIn(11, ids)

    def test_search_combined_criteria_returns_400(self):
        resp = self.client.post(
            "/ingredients/search", json={"names": ["a"], "ids": [1]}
        )
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)

    def test_search_missing_body_returns_400(self):
        # no JSON body -> error
        resp = self.client.post("/ingredients/search")
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
