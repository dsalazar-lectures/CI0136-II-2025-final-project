"""
Unit tests for API Recipes Schema
Tests the integration with TheMealDB API using the Adapter pattern
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os

# Add src to path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
)

from src.Database.Recipes import APIRecipesSchema
from src.Database.Recipes.TheMealDBAdapter import TheMealDBAdapter
from src.Database.Recipes.TheMealDBService import TheMealDBService


class TestTheMealDBService(unittest.TestCase):
    """Tests for TheMealDBService class"""

    @patch("src.Database.Recipes.TheMealDBService.requests.get")
    def test_obtain_recipes_success(self, mock_get):
        """Test successful API call"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "meals": [
                {
                    "idMeal": "52772",
                    "strMeal": "Teriyaki Chicken Casserole",
                    "strCategory": "Chicken",
                    "strArea": "Japanese",
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        service = TheMealDBService()
        result = service.obtain_recipes("")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["idMeal"], "52772")
        self.assertEqual(result[0]["strMeal"], "Teriyaki Chicken Casserole")

    @patch("src.Database.Recipes.TheMealDBService.requests.get")
    def test_obtain_recipes_no_meals(self, mock_get):
        """Test API response with no meals"""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        service = TheMealDBService()
        result = service.obtain_recipes("")

        self.assertEqual(result, [])

    @patch("src.Database.Recipes.TheMealDBService.requests.get")
    def test_obtain_recipes_request_exception(self, mock_get):
        """Test API call with request exception"""
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        service = TheMealDBService()
        result = service.obtain_recipes("")

        self.assertEqual(result, [])

    @patch("src.Database.Recipes.TheMealDBService.requests.get")
    def test_obtain_recipes_http_error(self, mock_get):
        """Test API call with HTTP error"""
        import requests

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Not Found"
        )
        mock_get.return_value = mock_response

        service = TheMealDBService()
        result = service.obtain_recipes("")

        self.assertEqual(result, [])

    @patch("src.Database.Recipes.TheMealDBService.requests.get")
    def test_obtain_recipes_with_query(self, mock_get):
        """Test API call with search query"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"meals": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        service = TheMealDBService()
        service.obtain_recipes("chicken")

        # Verify the URL was constructed correctly
        mock_get.assert_called_once()
        call_args = mock_get.call_args[0][0]
        self.assertIn("chicken", call_args)


class TestTheMealDBAdapter(unittest.TestCase):
    """Tests for TheMealDBAdapter class"""

    def test_parse_recipe_complete(self):
        """Test parsing a complete recipe"""
        meal = {
            "idMeal": "52772",
            "strMeal": "Teriyaki Chicken Casserole",
            "strCategory": "Chicken",
            "strArea": "Japanese",
            "strIngredient1": "chicken",
            "strIngredient2": "soy sauce",
            "strIngredient3": "ginger",
            "strMeasure1": "500g",
            "strMeasure2": "2 tbsp",
            "strMeasure3": "1 tsp",
            "strInstructions": "Cook the chicken...",
        }

        adapter = TheMealDBAdapter()
        result = adapter.parse_recipe(meal)

        self.assertEqual(result["id"], "52772")
        self.assertEqual(result["name"], "Teriyaki Chicken Casserole")

        # Categories are stored as repr() strings
        categories = eval(result["categories"])
        self.assertIn("chicken", categories)
        self.assertIn("japanese", categories)

        # Ingredients are stored as repr() strings
        ingredients = eval(result["ingredients"])
        self.assertEqual(len(ingredients), 3)
        self.assertEqual(ingredients[0], "500g chicken")
        self.assertEqual(ingredients[1], "2 tbsp soy sauce")

        self.assertEqual(result["author"], "TheMealDB")
        self.assertEqual(result["portions"], 1)
        self.assertIsNone(result["duration"])

    def test_parse_recipe_missing_measures(self):
        """Test parsing recipe with missing measures"""
        meal = {
            "idMeal": "12345",
            "strMeal": "Simple Dish",
            "strCategory": "Vegetarian",
            "strIngredient1": "tomato",
            "strIngredient2": "onion",
            "strMeasure1": "",
            "strMeasure2": None,
            "strInstructions": "Mix everything",
        }

        adapter = TheMealDBAdapter()
        result = adapter.parse_recipe(meal)

        # Ingredients are stored as repr() strings
        ingredients = eval(result["ingredients"])
        self.assertEqual(ingredients[0], "tomato")
        self.assertEqual(ingredients[1], "onion")

    def test_parse_recipe_empty_ingredients(self):
        """Test parsing recipe with empty ingredients"""
        meal = {
            "idMeal": "12345",
            "strMeal": "Minimal Recipe",
            "strCategory": "Dessert",
            "strIngredient1": "sugar",
            "strIngredient2": "",
            "strIngredient3": None,
            "strMeasure1": "100g",
            "strInstructions": "Simple dessert",
        }

        adapter = TheMealDBAdapter()
        result = adapter.parse_recipe(meal)

        # Ingredients are stored as repr() strings
        ingredients = eval(result["ingredients"])
        self.assertEqual(len(ingredients), 1)
        self.assertEqual(ingredients[0], "100g sugar")

    def test_parse_recipe_no_category(self):
        """Test parsing recipe without category"""
        meal = {
            "idMeal": "99999",
            "strMeal": "Mystery Meal",
            "strIngredient1": "ingredient",
            "strMeasure1": "1 unit",
            "strInstructions": "Do something",
        }

        adapter = TheMealDBAdapter()
        result = adapter.parse_recipe(meal)

        # Categories are stored as repr() strings
        categories = eval(result["categories"])
        self.assertEqual(categories, [])

    def test_parse_recipe_default_values(self):
        """Test that default values are set correctly"""
        meal = {
            "idMeal": "11111",
            "strMeal": "Test Recipe",
            "strIngredient1": "test",
            "strMeasure1": "1",
        }

        adapter = TheMealDBAdapter()
        result = adapter.parse_recipe(meal)

        self.assertEqual(result["calificationsSumatory"], 0)
        self.assertEqual(result["calificationsAmount"], 0)
        self.assertEqual(result["usersUsedRecipe"], 0)

    def test_extract_categories(self):
        """Test category extraction"""
        meal = {
            "strCategory": "Chicken",
            "strArea": "Japanese",
        }

        adapter = TheMealDBAdapter()
        categories = adapter._extract_categories(meal)

        self.assertEqual(len(categories), 2)
        self.assertIn("chicken", categories)
        self.assertIn("japanese", categories)

    def test_extract_ingredients(self):
        """Test ingredient extraction"""
        meal = {
            "strIngredient1": "chicken",
            "strIngredient2": "rice",
            "strIngredient3": "",
            "strMeasure1": "500g",
            "strMeasure2": "",
            "strMeasure3": "",
        }

        adapter = TheMealDBAdapter()
        ingredients = adapter._extract_ingredients(meal)

        self.assertEqual(len(ingredients), 2)
        self.assertEqual(ingredients[0], "500g chicken")
        self.assertEqual(ingredients[1], "rice")

    @patch.object(TheMealDBService, "obtain_recipes")
    def test_get_raw_data(self, mock_obtain):
        """Test get_raw_data delegates to service"""
        mock_obtain.return_value = [{"idMeal": "123"}]

        adapter = TheMealDBAdapter()
        result = adapter.get_raw_data()

        mock_obtain.assert_called_once_with("")
        self.assertEqual(result, [{"idMeal": "123"}])


class TestWriteApiRecipes(unittest.TestCase):
    """Tests for write_api_recipes function"""

    @patch("builtins.open", new_callable=mock_open)
    @patch("src.Database.Recipes.APIRecipesSchema.csv.DictWriter")
    def test_write_api_recipes(self, mock_dict_writer, mock_file):
        """Test writing recipes to CSV"""
        parsed_recipes = [
            {
                "id": "123",
                "name": "Test Recipe",
                "categories": "['chicken', 'asian']",  # Now it's a string
                "ingredients": "['chicken', 'soy sauce']",  # Now it's a string
                "duration": None,
                "instructions": "Cook it",
                "portions": 1,
                "author": "TheMealDB",
                "calificationsSumatory": 0,
                "calificationsAmount": 0,
                "usersUsedRecipe": 0,
            }
        ]

        mock_writer = MagicMock()
        mock_dict_writer.return_value = mock_writer

        APIRecipesSchema.write_api_recipes(parsed_recipes)

        # Verify file was opened
        mock_file.assert_called_once()
        # Verify writer was created
        mock_dict_writer.assert_called_once()
        # Verify header was written
        mock_writer.writeheader.assert_called_once()
        # Verify recipe was written
        self.assertEqual(mock_writer.writerow.call_count, 1)

    @patch("builtins.open", new_callable=mock_open)
    @patch("src.Database.Recipes.APIRecipesSchema.csv.DictWriter")
    def test_write_api_recipes_multiple(self, mock_dict_writer, mock_file):
        """Test writing multiple recipes to CSV"""
        parsed_recipes = [
            {
                "id": "1",
                "name": "Recipe 1",
                "categories": "['cat1']",  # Now it's a string
                "ingredients": "['ing1']",  # Now it's a string
                "duration": None,
                "instructions": "Instructions 1",
                "portions": 1,
                "author": "TheMealDB",
                "calificationsSumatory": 0,
                "calificationsAmount": 0,
                "usersUsedRecipe": 0,
            },
            {
                "id": "2",
                "name": "Recipe 2",
                "categories": "['cat2']",  # Now it's a string
                "ingredients": "['ing2']",  # Now it's a string
                "duration": None,
                "instructions": "Instructions 2",
                "portions": 1,
                "author": "TheMealDB",
                "calificationsSumatory": 0,
                "calificationsAmount": 0,
                "usersUsedRecipe": 0,
            },
        ]

        mock_writer = MagicMock()
        mock_dict_writer.return_value = mock_writer

        APIRecipesSchema.write_api_recipes(parsed_recipes)

        # Verify both recipes were written
        self.assertEqual(mock_writer.writerow.call_count, 2)


class TestLoadApiRecipes(unittest.TestCase):
    """Tests for load_api_recipes function"""

    @patch("src.Database.Recipes.APIRecipesSchema.Recipe")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="id,name,categories,ingredients,duration,instructions,portions,author,calificationsSumatory,calificationsAmount,usersUsedRecipe\n123,Test Recipe,['chicken'],['chicken'],None,Cook it,1,TheMealDB,0,0,0\n",
    )
    @patch.object(TheMealDBAdapter, "get_raw_data")
    @patch.object(TheMealDBAdapter, "parse_recipe")
    @patch("src.Database.Recipes.APIRecipesSchema.write_api_recipes")
    def test_load_api_recipes(
        self, mock_write, mock_parse, mock_get_raw, mock_file, mock_recipe
    ):
        """Test loading recipes from CSV"""
        # Mock the adapter methods
        mock_get_raw.return_value = [{"idMeal": "123"}]
        mock_parse.return_value = {
            "id": "123",
            "name": "Test Recipe",
            "categories": "['chicken']",
            "ingredients": "['chicken']",
            "duration": None,
            "instructions": "Cook it",
            "portions": 1,
            "author": "TheMealDB",
            "calificationsSumatory": 0,
            "calificationsAmount": 0,
            "usersUsedRecipe": 0,
        }

        # Clear the global list first
        APIRecipesSchema.api_recipes.clear()

        # Call the function
        APIRecipesSchema.load_api_recipes()

        # Verify adapter methods were called
        mock_get_raw.assert_called_once()
        mock_parse.assert_called_once()

        # Verify write was called
        mock_write.assert_called_once()

        # Verify Recipe constructor was called
        mock_recipe.assert_called()


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete flow"""

    @patch("src.Database.Recipes.APIRecipesSchema.write_api_recipes")
    @patch.object(TheMealDBService, "obtain_recipes")
    def test_full_integration_flow(self, mock_obtain, mock_write):
        """Test complete flow from API to CSV"""
        # Mock API response
        mock_obtain.return_value = [
            {
                "idMeal": "52772",
                "strMeal": "Teriyaki Chicken",
                "strCategory": "Chicken",
                "strArea": "Japanese",
                "strIngredient1": "chicken",
                "strMeasure1": "500g",
                "strInstructions": "Cook it",
            }
        ]

        # Simulate the flow
        adapter = TheMealDBAdapter()
        meals = adapter.get_raw_data()

        if meals:
            parsed_recipes = [adapter.parse_recipe(meal) for meal in meals]
            mock_write(parsed_recipes)

        # Verify the flow
        mock_obtain.assert_called_once()
        mock_write.assert_called_once()

        # Verify parsed recipe structure
        parsed = parsed_recipes[0]
        self.assertEqual(parsed["id"], "52772")
        self.assertEqual(parsed["name"], "Teriyaki Chicken")
        self.assertEqual(parsed["author"], "TheMealDB")

        # Categories and ingredients are stored as repr() strings
        categories = eval(parsed["categories"])
        self.assertIn("chicken", categories)
        self.assertIn("japanese", categories)

    @patch.object(TheMealDBService, "obtain_recipes")
    def test_adapter_integration(self, mock_obtain):
        """Test adapter correctly integrates with service"""
        mock_obtain.return_value = [
            {
                "idMeal": "123",
                "strMeal": "Test Meal",
                "strCategory": "Test",
                "strIngredient1": "ingredient",
                "strMeasure1": "1 cup",
            }
        ]

        adapter = TheMealDBAdapter()
        raw_data = adapter.get_raw_data()
        parsed = adapter.parse_recipe(raw_data[0])

        self.assertEqual(parsed["id"], "123")
        self.assertEqual(parsed["name"], "Test Meal")

        # Ingredients are stored as repr() strings
        ingredients = eval(parsed["ingredients"])
        self.assertIn("1 cup ingredient", ingredients)


if __name__ == "__main__":
    unittest.main()
