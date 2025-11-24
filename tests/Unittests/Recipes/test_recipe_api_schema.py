"""
Unit tests for API Recipes Schema
Tests the integration with TheMealDB API
"""

import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from src.Database.Recipes import APIRecipesSchema


class TestGetApiData(unittest.TestCase):
    """Tests for get_api_data function"""

    @patch("src.Database.Recipes.APIRecipesSchema.requests.get")
    def test_get_api_data_success(self, mock_get):
        """Test successful API call"""
        # Mock successful response
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

        result = APIRecipesSchema.get_api_data()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["idMeal"], "52772")
        self.assertEqual(result[0]["strMeal"], "Teriyaki Chicken Casserole")

    @patch("src.Database.Recipes.APIRecipesSchema.requests.get")
    def test_get_api_data_no_meals(self, mock_get):
        """Test API response with no meals"""
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = APIRecipesSchema.get_api_data()

        self.assertEqual(result, [])

    @patch("src.Database.Recipes.APIRecipesSchema.requests.get")
    def test_get_api_data_request_exception(self, mock_get):
        """Test API call with request exception"""
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        result = APIRecipesSchema.get_api_data()

        self.assertEqual(result, [])

    @patch("src.Database.Recipes.APIRecipesSchema.requests.get")
    def test_get_api_data_http_error(self, mock_get):
        """Test API call with HTTP error"""
        import requests
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        result = APIRecipesSchema.get_api_data()

        self.assertEqual(result, [])


class TestParseRecipe(unittest.TestCase):
    """Tests for parse_recipe function"""

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

        result = APIRecipesSchema.parse_recipe(meal)

        self.assertEqual(result["id"], "52772")
        self.assertEqual(result["name"], "Teriyaki Chicken Casserole")
        self.assertEqual(result["categories"], ["Chicken", "Japanese"])
        self.assertEqual(len(result["ingredients"]), 3)
        self.assertEqual(result["ingredients"][0], "500g chicken")
        self.assertEqual(result["ingredients"][1], "2 tbsp soy sauce")
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

        result = APIRecipesSchema.parse_recipe(meal)

        self.assertEqual(result["ingredients"][0], "tomato")
        self.assertEqual(result["ingredients"][1], "onion")

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

        result = APIRecipesSchema.parse_recipe(meal)

        self.assertEqual(len(result["ingredients"]), 1)
        self.assertEqual(result["ingredients"][0], "100g sugar")

    def test_parse_recipe_no_category(self):
        """Test parsing recipe without category"""
        meal = {
            "idMeal": "99999",
            "strMeal": "Mystery Meal",
            "strIngredient1": "ingredient",
            "strMeasure1": "1 unit",
            "strInstructions": "Do something",
        }

        result = APIRecipesSchema.parse_recipe(meal)

        self.assertEqual(result["categories"], [])

    def test_parse_recipe_default_values(self):
        """Test that default values are set correctly"""
        meal = {
            "idMeal": "11111",
            "strMeal": "Test Recipe",
            "strIngredient1": "test",
            "strMeasure1": "1",
        }

        result = APIRecipesSchema.parse_recipe(meal)

        self.assertEqual(result["calificationsSumatory"], 0)
        self.assertEqual(result["calificationsAmount"], 0)
        self.assertEqual(result["usersUsedRecipe"], 0)


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
                "categories": ["Chicken", "Asian"],
                "ingredients": ["chicken", "soy sauce"],
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
                "categories": ["Cat1"],
                "ingredients": ["ing1"],
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
                "categories": ["Cat2"],
                "ingredients": ["ing2"],
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

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="id,name,categories,ingredients,duration,instructions,portions,author,calificationsSumatory,calificationsAmount,usersUsedRecipe\n123,Test Recipe,['Chicken'],['chicken'],None,Cook it,1,TheMealDB,0,0,0\n",
    )
    @patch("src.Database.Recipes.APIRecipesSchema.Recipe")
    def test_load_api_recipes(self, mock_recipe, mock_file):
        """Test loading recipes from CSV"""
        # Clear the global list first
        APIRecipesSchema.api_recipes.clear()

        APIRecipesSchema.load_api_recipes()

        # Verify file was opened
        mock_file.assert_called_once()
        # Verify Recipe constructor was called
        mock_recipe.assert_called_once()


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete flow"""

    @patch("src.Database.Recipes.APIRecipesSchema.write_api_recipes")
    @patch("src.Database.Recipes.APIRecipesSchema.get_api_data")
    def test_full_integration_flow(self, mock_get_api, mock_write):
        """Test complete flow from API to CSV"""
        # Mock API response
        mock_get_api.return_value = [
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

        # This would normally happen in the module
        meals = mock_get_api()
        if meals:
            parsed_recipes = [APIRecipesSchema.parse_recipe(meal) for meal in meals]
            mock_write(parsed_recipes)

        # Verify the flow
        mock_get_api.assert_called_once()
        mock_write.assert_called_once()
        
        # Verify parsed recipe structure
        parsed = parsed_recipes[0]
        self.assertEqual(parsed["id"], "52772")
        self.assertEqual(parsed["name"], "Teriyaki Chicken")
        self.assertEqual(parsed["author"], "TheMealDB")


if __name__ == "__main__":
    unittest.main()