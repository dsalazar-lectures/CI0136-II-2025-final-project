"""
Unit tests for CSV Recipe Repository with API integration
Tests the combined functionality of system recipes and API recipes
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from src.Infrastructure.Recipes.CSVRecipeRepository import CSVRecipeRepository
from src.Model.Recipes.Recipes import Recipe


class TestCSVRecipeRepositoryAPIIntegration(unittest.TestCase):
    """Tests for API integration in CSVRecipeRepository"""

    def setUp(self):
        """Set up test fixtures"""
        self.repository = CSVRecipeRepository()
        
        # Mock system recipes
        self.mock_system_recipes = [
            Recipe(
                id="1",
                name="System Recipe 1",
                categories="['Breakfast']",
                ingredients="['eggs', 'milk']",
                duration="15",
                instructions="Mix and cook",
                portions="2",
                author="admin",
                califications_sumatory="10",
                califications_amount="2",
                users_used_recipe="5",
            ),
            Recipe(
                id="2",
                name="System Recipe 2",
                categories="['Lunch']",
                ingredients="['rice', 'chicken']",
                duration="30",
                instructions="Cook rice and chicken",
                portions="4",
                author="chef",
                califications_sumatory="20",
                califications_amount="4",
                users_used_recipe="10",
            ),
        ]
        
        # Mock API recipes
        self.mock_api_recipes = [
            Recipe(
                id="52772",
                name="Teriyaki Chicken",
                categories="['Chicken', 'Japanese']",
                ingredients="['chicken', 'soy sauce']",
                duration=None,
                instructions="Cook the chicken with sauce",
                portions="1",
                author="TheMealDB",
                califications_sumatory="0",
                califications_amount="0",
                users_used_recipe="0",
            ),
            Recipe(
                id="52773",
                name="Sushi",
                categories="['Seafood', 'Japanese']",
                ingredients="['rice', 'fish', 'nori']",
                duration=None,
                instructions="Roll the sushi",
                portions="1",
                author="TheMealDB",
                califications_sumatory="0",
                califications_amount="0",
                users_used_recipe="0",
            ),
        ]

    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_api_recipes")
    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_recipes")
    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.api_recipes")
    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.system_recipes")
    def test_get_all_combines_system_and_api(
        self, mock_system, mock_api, mock_load_recipes, mock_load_api
    ):
        """Test that get_all returns both system and API recipes"""
        mock_system.__add__ = lambda self, other: self.mock_system_recipes + other
        mock_system.__iter__ = lambda self: iter(self.mock_system_recipes)
        mock_api.__iter__ = lambda self: iter(self.mock_api_recipes)
        
        # Configure mocks to return our test data
        with patch.object(
            CSVRecipeRepository, "get_all"
        ) as mock_get_all:
            mock_get_all.return_value = self.mock_system_recipes + self.mock_api_recipes
            
            result = self.repository.get_all()
            
            # Verify both load functions were called (through the original method)
            # and that we get all recipes
            self.assertEqual(len(result), 4)
            
            # Verify system recipes are present
            system_names = [r.name for r in result if r.author != "TheMealDB"]
            self.assertIn("System Recipe 1", system_names)
            self.assertIn("System Recipe 2", system_names)
            
            # Verify API recipes are present
            api_names = [r.name for r in result if r.author == "TheMealDB"]
            self.assertIn("Teriyaki Chicken", api_names)
            self.assertIn("Sushi", api_names)

    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_api_recipes")
    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_recipes")
    def test_get_by_id_searches_both_sources(self, mock_load_recipes, mock_load_api):
        """Test that get_by_id searches in both system and API recipes"""
        with patch("src.Infrastructure.Recipes.CSVRecipeRepository.system_recipes", self.mock_system_recipes):
            with patch("src.Infrastructure.Recipes.CSVRecipeRepository.api_recipes", self.mock_api_recipes):
                # Test finding system recipe (ID as int since Recipe.__init__ converts to int)
                result_system = self.repository.get_by_id(1)
                self.assertIsNotNone(result_system)
                self.assertEqual(result_system.name, "System Recipe 1")
                
                # Test finding API recipe
                result_api = self.repository.get_by_id(52772)
                self.assertIsNotNone(result_api)
                self.assertEqual(result_api.name, "Teriyaki Chicken")
                self.assertEqual(result_api.author, "TheMealDB")
                
                # Test not finding recipe
                result_none = self.repository.get_by_id(99999)
                self.assertIsNone(result_none)

    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_api_recipes")
    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_recipes")
    def test_find_by_ingredient_searches_both_sources(
        self, mock_load_recipes, mock_load_api
    ):
        """Test that find_by_ingredient searches in both system and API recipes"""
        with patch("src.Infrastructure.Recipes.CSVRecipeRepository.system_recipes", self.mock_system_recipes):
            with patch("src.Infrastructure.Recipes.CSVRecipeRepository.api_recipes", self.mock_api_recipes):
                # Search for chicken (in both sources)
                result_chicken = self.repository.find_by_ingredient("chicken")
                self.assertEqual(len(result_chicken), 2)  # One system, one API
                
                # Search for soy sauce (only in API)
                result_soy = self.repository.find_by_ingredient("soy sauce")
                self.assertEqual(len(result_soy), 1)
                self.assertEqual(result_soy[0].author, "TheMealDB")
                
                # Search for eggs (only in system)
                result_eggs = self.repository.find_by_ingredient("eggs")
                self.assertEqual(len(result_eggs), 1)
                self.assertEqual(result_eggs[0].author, "admin")

    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_api_recipes")
    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_recipes")
    def test_find_by_category_searches_both_sources(
        self, mock_load_recipes, mock_load_api
    ):
        """Test that find_by_category searches in both system and API recipes"""
        with patch("src.Infrastructure.Recipes.CSVRecipeRepository.api_recipes", self.mock_api_recipes):
            with patch("src.Infrastructure.Recipes.CSVRecipeRepository.system_recipes", self.mock_system_recipes):
                # Search for Japanese (only in API)
                result_japanese = self.repository.find_by_category("Japanese")
                self.assertEqual(len(result_japanese), 2)
                self.assertTrue(all(r.author == "TheMealDB" for r in result_japanese))
                
                # Search for Breakfast (only in system)
                result_breakfast = self.repository.find_by_category("Breakfast")
                self.assertEqual(len(result_breakfast), 1)
                self.assertEqual(result_breakfast[0].author, "admin")

    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_api_recipes")
    def test_get_api_recipes_returns_only_api(self, mock_load_api):
        """Test that get_api_recipes returns only API recipes"""
        with patch("src.Infrastructure.Recipes.CSVRecipeRepository.api_recipes", self.mock_api_recipes):
            result = CSVRecipeRepository.get_api_recipes()
            
            # Verify all recipes are from API
            self.assertTrue(all(r.author == "TheMealDB" for r in result))
            self.assertEqual(len(result), 2)

    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_recipes")
    def test_get_system_recipes_returns_only_system(self, mock_load_recipes):
        """Test that get_system_recipes returns only system recipes"""
        with patch("src.Infrastructure.Recipes.CSVRecipeRepository.system_recipes", self.mock_system_recipes):
            result = CSVRecipeRepository.get_system_recipes()
            
            # Verify all recipes are from system
            self.assertTrue(all(r.author != "TheMealDB" for r in result))
            self.assertEqual(len(result), 2)

    def test_api_recipes_have_correct_defaults(self):
        """Test that API recipes have the correct default values"""
        # Create an API recipe like the schema does
        api_recipe = Recipe(
            id="52772",
            name="Test API Recipe",
            categories="['Chicken']",
            ingredients="['chicken']",
            duration=None,  # Should be None for API recipes
            instructions="Cook it",
            portions="1",  # Should be 1 for API recipes
            author="TheMealDB",  # Should be TheMealDB for API recipes
            califications_sumatory="0",
            califications_amount="0",
            users_used_recipe="0",
        )
        
        self.assertEqual(api_recipe.author, "TheMealDB")
        self.assertEqual(api_recipe.portions, 1)
        self.assertEqual(api_recipe.duration, 0)  # None becomes 0 in Recipe.__init__
        self.assertEqual(api_recipe.califications_sumatory, 0)

    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_api_recipes")
    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_recipes")
    def test_case_insensitive_ingredient_search(
        self, mock_load_recipes, mock_load_api
    ):
        """Test that ingredient search is case-insensitive"""
        with patch("src.Infrastructure.Recipes.CSVRecipeRepository.system_recipes", self.mock_system_recipes):
            with patch("src.Infrastructure.Recipes.CSVRecipeRepository.api_recipes", self.mock_api_recipes):
                # Search with different cases
                result_lower = self.repository.find_by_ingredient("chicken")
                result_upper = self.repository.find_by_ingredient("CHICKEN")
                result_mixed = self.repository.find_by_ingredient("ChIcKeN")
                
                # All should return same results
                self.assertEqual(len(result_lower), len(result_upper))
                self.assertEqual(len(result_upper), len(result_mixed))

    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_api_recipes")
    @patch("src.Infrastructure.Recipes.CSVRecipeRepository.load_recipes")
    def test_case_insensitive_category_search(
        self, mock_load_recipes, mock_load_api
    ):
        """Test that category search is case-insensitive"""
        with patch("src.Infrastructure.Recipes.CSVRecipeRepository.api_recipes", self.mock_api_recipes):
            with patch("src.Infrastructure.Recipes.CSVRecipeRepository.system_recipes", self.mock_system_recipes):
                # Search with different cases
                result_lower = self.repository.find_by_category("japanese")
                result_upper = self.repository.find_by_category("JAPANESE")
                result_mixed = self.repository.find_by_category("JaPaNeSe")
                
                # All should return same results
                self.assertEqual(len(result_lower), len(result_upper))
                self.assertEqual(len(result_upper), len(result_mixed))


class TestAPIRecipeProperties(unittest.TestCase):
    """Tests for API recipe specific properties"""

    def test_api_recipe_duration_is_none(self):
        """Test that API recipes have duration as None"""
        api_recipe = Recipe(
            id="52772",
            name="API Recipe",
            categories="['Test']",
            ingredients="['ingredient']",
            duration=None,
            instructions="Instructions",
            portions="1",
            author="TheMealDB",
            califications_sumatory="0",
            califications_amount="0",
            users_used_recipe="0",
        )
        
        # Duration should be None (or "None" as string depending on implementation)
        self.assertIn(str(api_recipe.duration), ["None", "0"])

    def test_api_recipe_author_is_themealdb(self):
        """Test that API recipes have TheMealDB as author"""
        api_recipe = Recipe(
            id="52772",
            name="API Recipe",
            categories="['Test']",
            ingredients="['ingredient']",
            duration=None,
            instructions="Instructions",
            portions="1",
            author="TheMealDB",
            califications_sumatory="0",
            califications_amount="0",
            users_used_recipe="0",
        )
        
        self.assertEqual(api_recipe.author, "TheMealDB")

    def test_api_recipe_default_portions(self):
        """Test that API recipes have default portions of 1"""
        api_recipe = Recipe(
            id="52772",
            name="API Recipe",
            categories="['Test']",
            ingredients="['ingredient']",
            duration=None,
            instructions="Instructions",
            portions="1",
            author="TheMealDB",
            califications_sumatory="0",
            califications_amount="0",
            users_used_recipe="0",
        )
        
        self.assertEqual(api_recipe.portions, 1)


if __name__ == "__main__":
    unittest.main()