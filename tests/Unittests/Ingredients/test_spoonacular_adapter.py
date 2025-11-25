import unittest
from unittest.mock import Mock
from src.Infrastructure.Ingredients.external.SpoonacularAPIService import (
    SpoonacularAPIService,
)
from src.Infrastructure.Ingredients.external.SpoonacularIngredientAdapter import (
    SpoonacularIngredientAdapter,
)
from src.Model.Ingredients.BaseIngredient import BaseIngredient
from tests.Mocks.Ingredients.spoonacular_data import (
    MOCK_SPOONACULAR_APPLE_INFO,
    MOCK_SPOONACULAR_OIL_INFO,
)


class TestSpoonacularIngredientAdapter(unittest.TestCase):

    def setUp(self):
        """Configuración para cada prueba, creando el mock del servicio API."""
        self.mock_api_service = Mock(spec=SpoonacularAPIService)
        self.adapter = SpoonacularIngredientAdapter(api_service=self.mock_api_service)

    def test_map_categories_simple_aisle(self):
        """Verifica que un 'aisle' simple (e.g., Produce) se mapee correctamente."""

        mock_data = MOCK_SPOONACULAR_APPLE_INFO
        categories = self.adapter._map_categories(mock_data)

        self.assertEqual(categories, ["produce"])

    def test_map_categories_compound_aisle(self):
        """Verifica que un 'aisle' compuesto (e.g., Oil, Vinegar, Salad Dressing) se mapee correctamente."""

        mock_data = MOCK_SPOONACULAR_OIL_INFO

        categories = self.adapter._map_categories(mock_data)

        self.assertEqual(categories, ["oil,-vinegar,-salad-dressing"])

    def test_map_categories_handles_no_aisle(self):
        """Verifica que el mapeo retorne una lista vacía si 'aisle' no existe."""
        mock_data = {
            "name": "Water",
        }
        categories = self.adapter._map_categories(mock_data)
        self.assertEqual(categories, [])

    def test_search_ingredient_not_found_returns_none(self):
        """Testea cuando el servicio Spoonacular no encuentra el ingrediente."""
        self.mock_api_service.fetch_ingredient_data.return_value = None

        result = self.adapter.search_ingredient("nonexistent_food")

        self.assertIsNone(result)
        self.mock_api_service.fetch_ingredient_data.assert_called_once_with(
            "nonexistent_food"
        )

    def test_search_ingredient_correctly_maps_fields(self):
        """Verifica que todos los campos del modelo BaseIngredient se llenen correctamente."""

        self.mock_api_service.fetch_ingredient_data.return_value = (
            MOCK_SPOONACULAR_APPLE_INFO
        )

        result = self.adapter.search_ingredient("apple")

        self.assertEqual(result.name, "Apple")

        self.assertEqual(result.categories, ["produce"])

        self.assertTrue(result.id >= 10000)
        self.assertIsInstance(result, BaseIngredient)


if __name__ == "__main__":
    unittest.main()
