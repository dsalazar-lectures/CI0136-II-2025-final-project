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

    def __init__(
        self,
        name="Test Recipe",
        author="Chef 1",
        categories=None,
        duration=30,
        califications_sumatory=40,
        califications_amount=10,
        ingredients=None,
        portions=4,
    ):
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
            MockRecipe(author="John Doe"),
        ]

        filtered = author_filter.filter(recipes)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(r.author == "John Doe" for r in filtered))

    def test_author_filter_case_sensitive(self):
        """Test author filter is case sensitive"""
        base = BaseRecipeFilter()
        author_filter = AuthorFilter(base, "JOHN DOE")

        recipes = [MockRecipe(author="john doe"), MockRecipe(author="Jane Smith")]

        filtered = author_filter.filter(recipes)

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].author, "john doe")

    def test_author_filter_no_matches(self):
        """Test author filters returns an empty list if there are no matches"""
        base = BaseRecipeFilter()
        author_filter = AuthorFilter(base, "NA")

        recipes = [MockRecipe(author="John Doe"), MockRecipe(author="Jane Smith")]

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
            MockRecipe(categories=["dessert"]),
        ]

        filtered = category_filter.filter(recipes)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(r.categories == ["dessert"] for r in filtered))

    def test_category_filter_multiple_categories(self):
        """Test category filter finds recipes with multiple categories"""
        base = BaseRecipeFilter()
        category_filter = CategoryFilter(base, ["dessert", "breakfast"])

        recipes = [
            MockRecipe(categories=["dessert"]),
            MockRecipe(categories=["breakfast"]),
            MockRecipe(categories=["dinner"]),
        ]

        filtered = category_filter.filter(recipes)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(
            all(r.categories == ["dessert"] or ["breakfast"] for r in filtered)
        )

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
            MockRecipe(duration=15),
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


class TestCalificationFilter(unittest.TestCase):

    def test_calification_filter_minimum_rating(self):
        """Test rating filter includes minimum rating"""
        base = BaseRecipeFilter()
        calification_filter = CalificationFilter(base, 4.0)

        recipes = [
            MockRecipe(califications_sumatory=40, califications_amount=10),  # 4.0
            MockRecipe(califications_sumatory=45, califications_amount=10),  # 4.5
            MockRecipe(califications_sumatory=30, califications_amount=10),  # 3.0
        ]

        filtered = calification_filter.filter(recipes)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(r.califications_sumatory >= 40 for r in filtered))

    def test_calification_filter_exact_rating(self):
        """Test rating filter includes recipes with exact rating"""
        base = BaseRecipeFilter()
        calification_filter = CalificationFilter(base, 4.0)

        recipes = [MockRecipe(califications_sumatory=40, califications_amount=10)]

        filtered = calification_filter.filter(recipes)

        self.assertEqual(len(filtered), 1)
        self.assertTrue(filtered[0].califications_sumatory == 40)


class TestIngredientsFilter(unittest.TestCase):

    def test_ingredients_filter_single_ingredient(self):
        """Test ingredient filter finds recipes with an specific ingredient"""
        base = BaseRecipeFilter()
        ingredients_filter = IngredientsFilter(base, ["flour"])

        recipes = [
            MockRecipe(ingredients=["flour", "sugar"]),
            MockRecipe(ingredients=["milk", "eggs"]),
            MockRecipe(ingredients=["flour", "butter"]),
        ]

        filtered = ingredients_filter.filter(recipes)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(all("flour" in r.ingredients for r in filtered))

    def test_ingredients_filter_partial_match(self):
        """Test filter matches partial ingredients"""
        base = BaseRecipeFilter()
        ingredients_filter = IngredientsFilter(base, ["choc"])

        recipes = [
            MockRecipe(ingredients=["chocolate chips"]),
            MockRecipe(ingredients=["vanilla"]),
        ]

        filtered = ingredients_filter.filter(recipes)

        self.assertEqual(len(filtered), 1)
        self.assertTrue(filtered[0].ingredients == ["chocolate chips"])


class TestPortionsFilter(unittest.TestCase):

    def test_portions_filter_range(self):
        """Test portion filter filters by range"""
        base = BaseRecipeFilter()
        portions_filter = PortionsFilter(base, "2-6")

        recipes = [
            MockRecipe(portions=2),
            MockRecipe(portions=4),
            MockRecipe(portions=8),
            MockRecipe(portions=1),
        ]

        filtered = portions_filter.filter(recipes)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(r.portions == 2 or 4 for r in filtered))

    def test_portions_filter_minimum_only(self):
        """Test filter accepts min portions only"""
        base = BaseRecipeFilter()
        portions_filter = PortionsFilter(base, "4-")

        recipes = [
            MockRecipe(portions=2),
            MockRecipe(portions=4),
            MockRecipe(portions=10),
        ]

        filtered = portions_filter.filter(recipes)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(r.portions == 4 or 10 for r in filtered))

    def test_portions_filter_exact_value(self):
        """Test filter accepts exact portion"""
        base = BaseRecipeFilter()
        portions_filter = PortionsFilter(base, "4")

        recipes = [MockRecipe(portions=4), MockRecipe(portions=2)]

        filtered = portions_filter.filter(recipes)

        self.assertEqual(len(filtered), 1)
        self.assertTrue(filtered[0].portions == 4)


class TestDislikesFilter(unittest.TestCase):

    def test_dislikes_filter_excludes_ingredients(self):
        """Test dislike filters exclude depending on ingredient"""
        base = BaseRecipeFilter()
        dislikes_filter = DislikesFilter(base, ["chocolate"])

        recipes = [
            MockRecipe(ingredients=["flour", "sugar"]),
            MockRecipe(ingredients=["peanuts", "chocolate"]),
            MockRecipe(ingredients=["almonds", "honey"]),
        ]

        filtered = dislikes_filter.filter(recipes)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(
            all(
                r.ingredients == ["flour", "sugar"] or ["almonds", "honey"]
                for r in filtered
            )
        )

    def test_dislikes_filter_partial_match(self):
        """Test filter detects partial ingredients"""
        base = BaseRecipeFilter()
        dislikes_filter = DislikesFilter(base, ["nut"])

        recipes = [
            MockRecipe(ingredients=["coconut milk"]),
            MockRecipe(ingredients=["flour"]),
        ]

        filtered = dislikes_filter.filter(recipes)

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].ingredients, ["flour"])

    def test_dislikes_filter_multiple_dislikes(self):
        """Test filter handles multiple undesired ingredients"""
        base = BaseRecipeFilter()
        dislikes_filter = DislikesFilter(base, ["flour", "butter"])

        recipes = [
            MockRecipe(ingredients=["flour", "eggs"]),
            MockRecipe(ingredients=["milk", "butter"]),
            MockRecipe(ingredients=["almonds", "honey"]),
        ]

        filtered = dislikes_filter.filter(recipes)

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].ingredients, ["almonds", "honey"])


class TestFilterComposer(unittest.TestCase):

    def test_filter_composer_single_filter(self):
        """Test FilterComposer applies one filter correctly"""
        composer = FilterComposer()
        recipes = [MockRecipe(author="John Doe"), MockRecipe(author="Jane Smith")]

        filter_criteria = {"author": "John Doe"}
        filtered = composer.apply_filters(recipes, filter_criteria)

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].author, "John Doe")

    def test_filter_composer_multiple_filters(self):
        """Test FilterComposer chains different filters"""
        composer = FilterComposer()
        recipes = [
            MockRecipe(author="John Doe", duration=20, categories=["dessert"]),
            MockRecipe(author="John Doe", duration=45, categories=["dessert"]),
            MockRecipe(author="Jane Smith", duration=20, categories=["dessert"]),
        ]

        filter_criteria = {"author": "John Doe", "duration": 30}
        filtered = composer.apply_filters(recipes, filter_criteria)

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].duration, 20)

    def test_filter_composer_empty_criteria(self):
        """Test FilterComposer returns all recipes if there is no criteria"""
        composer = FilterComposer()
        recipes = [MockRecipe(), MockRecipe(), MockRecipe()]

        filtered = composer.apply_filters(recipes, {})

        self.assertEqual(len(filtered), 3)

    def test_filter_composer_ignores_invalid_values(self):
        """Test FilterComposer ignores invalid values"""
        composer = FilterComposer()
        recipes = [MockRecipe(), MockRecipe()]

        filter_criteria = {"author": None, "duration": "", "category": ["dessert"]}
        filtered = composer.apply_filters(recipes, filter_criteria)

        self.assertEqual(len(filtered), 2)

    def test_filter_composer_complex_chain(self):
        """Integration test, complex filter chain"""
        composer = FilterComposer()
        recipes = [
            MockRecipe(
                author="John Doe",
                duration=25,
                categories=["dessert"],
                ingredients=["chocolate", "flour"],
                portions=4,
                califications_sumatory=45,
                califications_amount=10,
            ),
            MockRecipe(
                author="Jane Smith",
                duration=20,
                categories=["dessert"],
                ingredients=["vanilla", "sugar"],
                portions=6,
                califications_sumatory=30,
                califications_amount=10,
            ),
            MockRecipe(
                author="John Doe",
                duration=35,
                categories=["main course"],
                ingredients=["chicken", "rice"],
                portions=4,
                califications_sumatory=40,
                califications_amount=10,
            ),
        ]

        filter_criteria = {
            "author": "John Doe",
            "duration": 30,
            "category": ["dessert"],
            "ingredients": ["chocolate"],
            "rating": 4.0,
        }

        filtered = composer.apply_filters(recipes, filter_criteria)

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].author, "John Doe")
        self.assertTrue("chocolate" in filtered[0].ingredients)

    def test_filter_composer_with_dislikes(self):
        """Test FilterComposer handles dislike filter correctly"""
        composer = FilterComposer()
        recipes = [
            MockRecipe(ingredients=["flour", "eggs"]),
            MockRecipe(ingredients=["peanuts", "chocolate"]),
            MockRecipe(ingredients=["almonds", "honey"]),
        ]

        filter_criteria = {"dislikes": ["flour"]}
        filtered = composer.apply_filters(recipes, filter_criteria)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(
            all(
                r.ingredients == ["peanuts", "chocolate"] or ["almonds", "honey"]
                for r in filtered
            )
        )

    def test_filter_composer_all_filters_no_results(self):
        """Test FilterComposer returns an empty list if there are no matches"""
        composer = FilterComposer()
        recipes = [
            MockRecipe(author="John Doe", duration=50),
            MockRecipe(author="Jane Smith", duration=60),
        ]

        filter_criteria = {"author": "Bob Johnson", "duration": 30}

        filtered = composer.apply_filters(recipes, filter_criteria)

        self.assertEqual(len(filtered), 0)
