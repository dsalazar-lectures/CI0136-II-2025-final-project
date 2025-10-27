import unittest
from unittest.mock import patch, Mock
from flask import Flask
from src.API.Ingredients.IngredientsRoutes import ingredients_bp
from tests.Mocks.mock_ingredients import (
    MockIngredient,
    INGREDIENT_1, INGREDIENT_2, INGREDIENT_3,
    SIMPLE_INGREDIENT_1, SIMPLE_INGREDIENT_2, SIMPLE_INGREDIENT_3
)

class IngredientServiceTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(ingredients_bp)
        self.client = app.test_client()

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_get_all_ingredients_simplified(self, mock_service):
        """Test GET /ingredients?simple=true returns only id and name."""
        # Arrange: El servicio devuelve objetos de ingrediente completos
        mock_service.get_all_ingredients.return_value = [
            INGREDIENT_1,
            INGREDIENT_2,
            INGREDIENT_3,
        ]

        # Act: Petición con el parámetro simple=true
        response = self.client.get("/ingredients?simple=true")

        # Assert
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        expected_data = [SIMPLE_INGREDIENT_1, SIMPLE_INGREDIENT_2, SIMPLE_INGREDIENT_3]
        
        # Verifica que la respuesta JSON es la simplificada
        self.assertEqual(data, expected_data)
        mock_service.get_all_ingredients.assert_called_once()

        # --- TESTS DE BÚSQUEDA (SEARCH) ---

    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_search_by_names_success(self, mock_service):
        """Test POST /ingredients/search with valid 'names' criterion."""
        # Arrange: Configura side_effect para simular la búsqueda por nombre
        mock_service.get_ingredient_by_name.side_effect = lambda name: {
            "Butter": INGREDIENT_1,
            "Milk": INGREDIENT_2,
            "Water": None,
        }.get(name)

        # Act: Búsqueda de dos nombres válidos y uno no encontrado
        response = self.client.post("/ingredients/search", json={"names": ["Butter", "Milk", "Water"]})

        # Assert: 200 OK y verificación de resultados/no encontrados
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertEqual(len(data['results']), 2)
        self.assertEqual(data['results'][0]['name'], 'Butter')
        self.assertEqual(data['not_found'], ['Water'])


    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_search_by_ids_success(self, mock_service):
        """Test POST /ingredients/search with valid 'ids' criterion."""
        # Arrange: Configura side_effect para simular la búsqueda por ID
        mock_service.get_ingredient_by_id.side_effect = lambda id: {
            1: INGREDIENT_1,
            2: INGREDIENT_2,
            99: None,
        }.get(id)

        # Act: Búsqueda de dos IDs válidos y uno no encontrado
        response = self.client.post("/ingredients/search", json={"ids": [1, 2, 99]})

        # Assert
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertEqual(len(data['results']), 2)
        self.assertEqual(data['results'][0]['id'], 1)
        self.assertEqual(data['not_found'], [99])


    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_search_by_categories_success(self, mock_service):
        """Test POST /ingredients/search with valid 'categories' criterion."""
        # Arrange: Configura return_value para simular la lista de ingredientes por categoría
        mock_service.get_ingredients_by_category.return_value = [INGREDIENT_2, INGREDIENT_3]

        # Act: Búsqueda por categoría
        response = self.client.post("/ingredients/search", json={"categories": ["Dairy"]})

        # Assert
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertEqual(len(data['results']), 2)
        self.assertEqual(data['results'][0]['name'], 'Milk')
        mock_service.get_ingredients_by_category.assert_called_once_with('Dairy')


    @patch("src.API.Ingredients.IngredientsRoutes.ingredient_service")
    def test_search_names_simplified_body(self, mock_service):
        """Test POST /ingredients/search with names and {'simple': true} in body."""
        mock_service.get_ingredient_by_name.side_effect = lambda name: {
            "Butter": INGREDIENT_1,
        }.get(name)

        # Act: Petición con simple: true en el body
        response = self.client.post("/ingredients/search", json={"names": ["Butter"], "simple": True})
        
        # Assert: Verifica que la respuesta sea simplificada (solo id y name)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['results'], [SIMPLE_INGREDIENT_1])
        self.assertNotIn('categories', data['results'][0]) # Verifica que no tiene campos extra


    # --- TESTS DE ERRORES (MAL HECHAS) ---

    def test_search_mal_hecha_no_body(self):
        """Test POST /ingredients/search without a JSON body (mal hecho)."""
        # Debe fallar porque la función _get_request_data espera JSON
        response = self.client.post("/ingredients/search", data="not json", content_type='text/plain')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "Cuerpo JSON requerido")
        

    def test_search_mal_hecha_no_criteria(self):
        """Test POST /ingredients/search with an empty body (mal hecho)."""
        response = self.client.post("/ingredients/search", json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Se requiere un criterio de búsqueda", response.get_json()["error"])


    def test_search_mal_hecha_multiple_criteria(self):
        """Test POST /ingredients/search with names AND categories (mal hecho)."""
        response = self.client.post("/ingredients/search", json={"names": ["A"], "categories": ["B"]})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Solo se permite un criterio de búsqueda a la vez", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()