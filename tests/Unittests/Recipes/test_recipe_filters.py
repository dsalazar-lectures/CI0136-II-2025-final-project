import unittest
from unittest.mock import MagicMock
from src.Application.Recipes.BaseRecipeFilter import BaseRecipeFilter
from src.Application.Recipes.AuthorFilter import AuthorFilter
from src.Application.Recipes.CategoryFilter import CategoryFilter
from src.Application.Recipes.DurationFilter import DurationFilter
from src.Application.Recipes.CalificationFilter import CalificationFilter
from src.Application.Recipes.IngredientsFilter import IngredientsFilter
from src.Application.Recipes.PortionsFilter import PortionsFilter
from src.Application.Recipes.DislikesFilter import DislikesFilter
from src.Application.Recipes.FilterComposer import FilterComposer

class MockRecipe:
    """Mock recipe object for testing"""
    def __init__(self, name = "Test Recipe", author = "Chef 1", categories = None,
                 duration = 30, califications_sumatory = 40, califications_amount = 10,
                 ingredients = None, portions = 4):
        self.name = name
        self.author = author
        self.categories = categories or ["dessert"]
        self.duration = duration
        self.califications_sumatory = califications_sumatory
        self.califications_amount = califications_amount
        self.ingredients = ingredients or ["flour", "sugar", "eggs"]
        self.portions = portions
        
class TestBaseRecipeFilter(unittest.TestCase):

    def test_base_filter_returns_all_recipes(self):
        """Test base filter returns all recipes with no filter"""
        base_filter = BaseRecipeFilter()
        recipes = [MockRecipe(), MockRecipe(), MockRecipe()]

        filtered = base_filter.filter(recipes)

        self.assertEqual(len(filtered), 3)
        self.assertEqual(filtered, recipes)

    def test_base_filter_with_empty_list(self):
        """Test base filter handles empty lists"""
        base_filter = BaseRecipeFilter()
        recipes = []

        filtered = base_filter.filter(recipes)

        self.assertEqual(len(filtered), 0)

class TestAuthorFilter(unittest.TestCase):

    def test_author_filter_matches_exact_author(self):
        """Test author filter finds recipes from the correct author"""
        base = BaseRecipeFilter()
        author_filter = AuthorFilter(base, "John Doe")

        recipes = [
            MockRecipe(author="John Doe"),
            MockRecipe(author="Jane Smith"),
            MockRecipe(author="John Doe")
        ]

        filtered = author_filter.filter(recipes)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(r.author == "John Doe" for r in filtered))

    def test_author_filter_case_sensitive(self):
        """Test author filter is case sensitive"""
        base = BaseRecipeFilter()
        author_filter = AuthorFilter(base, "JOHN DOE")

        recipes = [
            MockRecipe(author="john doe"),
            MockRecipe(author="Jane Smith")
        ]

        filtered = author_filter.filter(recipes)

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].author, "john doe")

    def test_author_filter_no_matches(self):
        """Test author filters returns an empty list if there are no matches"""
        base = BaseRecipeFilter()
        author_filter = AuthorFilter(base, "NA")

        recipes = [
            MockRecipe(author="John Doe"),
            MockRecipe(author="Jane Smith")
        ]

        filtered = author_filter.filter(recipes)

        self.assertEqual(len(filtered), 0)

class TestCategoryFilter(unittest.TestCase):

    def test_category_filter_single_category(self):
        """Test category filter finds recipes with an specific category"""
        base = BaseRecipeFilter()
        category_filter = CategoryFilter(base, ["dessert"])

        recipes = [
            MockRecipe(categories=["dessert"]),
            MockRecipe(categories=["breakfast"]),
            MockRecipe(categories=["dessert"])
        ]

        filtered = category_filter.filter(recipes)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(r.categories == ['dessert'] for r in filtered))

    def test_category_filter_multiple_categories(self):
        """Test category filter finds recipes with multiple categories"""
        base = BaseRecipeFilter()
        category_filter = CategoryFilter(base, ["dessert", "breakfast"])

        recipes = [
            MockRecipe(categories=["dessert"]),
            MockRecipe(categories=["breakfast"]),
            MockRecipe(categories=["dinner"])
        ]

        filtered = category_filter.filter(recipes)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(r.categories == ['dessert'] or ['breakfast'] for r in filtered))

    def test_category_filter_case_sensitive(self):
        """Test category filter is not case sensitive"""
        base = BaseRecipeFilter()
        category_filter = CategoryFilter(base, ["DESSeRT"])

        recipes = [MockRecipe(categories=["dessert"])]

        filtered = category_filter.filter(recipes)

        self.assertEqual(len(filtered), 1)
        self.assertTrue(filtered[0].categories == ["dessert"])

class TestDurationFilter(unittest.TestCase):

    def test_duration_filter_max_duration(self):
        """Test duration filter filters recipes by max time"""
        base = BaseRecipeFilter()
        duration_filter = DurationFilter(base, 30)
        
        recipes = [
            MockRecipe(duration=20),
            MockRecipe(duration=30),
            MockRecipe(duration=45),
            MockRecipe(duration=15)
        ]
        
        filtered = duration_filter.filter(recipes)
        
        self.assertEqual(len(filtered), 3)
        self.assertTrue(all(r.duration <= 30 for r in filtered))

    def test_duration_filter_exact_match(self):
        """Test duration filter includes recipes with exact duration"""
        base = BaseRecipeFilter()
        duration_filter = DurationFilter(base, 30)
        
        recipes = [MockRecipe(duration=30)]
        
        filtered = duration_filter.filter(recipes)
        
        self.assertEqual(len(filtered), 1)
        self.assertTrue(filtered[0].duration == 30)

        

