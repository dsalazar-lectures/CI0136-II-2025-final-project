import unittest
import inspect
from typing import List, Optional
from src.Application.Menu.ICustomizedMenuService import ICustomizedMenuService
from src.Application.Menu.CustomizedMenuService import CustomizedMenuService


class FakeRecipe:
    """Mock recipe class for testing purposes"""
    def __init__(self, title: str, ingredients: List[str], categories: Optional[List[str]] = None, rating: int = 0):
        self.title = title
        self.ingredients = ingredients
        self.categories = categories or []
        self.rating = rating


class FakeRecipeService:
    """Mock recipe service for testing"""
    def __init__(self, recipes: List[FakeRecipe]):
        self._recipes = list(recipes)

    def get_all_recipes(self) -> List[FakeRecipe]:
        return list(self._recipes)

    def filter_recipes(self, criteria: dict) -> List[FakeRecipe]:
        cats = [c.lower().strip() for c in (criteria.get("categories") or [])]
        out = []
        for recipe in self._recipes:
            recipe_categories = [c.lower().strip() for c in (recipe.categories or [])]
            if set(cats) & set(recipe_categories):
                out.append(recipe)
        return out


def build_sut(recipes: List[FakeRecipe], require_all: bool = False) -> CustomizedMenuService:
    """Helper function to build the System Under Test"""
    return CustomizedMenuService(service=FakeRecipeService(recipes), require_all=require_all)


class TestICustomizedMenuServiceInterface(unittest.TestCase):
    """Test cases for the CustomizedMenuService interface"""
    
    def test_interface_signature(self):
        """Verify the interface declares recommend_by_favorites with correct signature"""
        self.assertTrue(hasattr(ICustomizedMenuService, "recommend_by_favorites"))
        sig = inspect.signature(ICustomizedMenuService.recommend_by_favorites)
        params = list(sig.parameters.values())
        self.assertEqual(params[0].name, "self")
        self.assertEqual(params[1].name, "favorites")
        self.assertEqual(params[2].name, "category")
        self.assertEqual(params[3].name, "limit")


class TestCustomizedMenuServiceBehavior(unittest.TestCase):
    """Test cases for CustomizedMenuService behavior"""

    def setUp(self):
        """Initialize test recipes"""
        self.recipes = [
            FakeRecipe("Pasta al Pollo", ["Pollo", "Pasta", "Tomate"], ["almuerzo"], rating=4),
            FakeRecipe("Ensalada Caprese", ["Tomate", "Albahaca", "Queso"], ["almuerzo", "cena"], rating=5),
            FakeRecipe("Tofu Salteado", ["Tofu", "Jengibre", "Ajo"], ["cena"], rating=3),
            FakeRecipe("Sopa de Verduras", ["Zanahoria", "Apio", "Tomate"], ["almuerzo"], rating=2),
            FakeRecipe("Pizza Margherita", ["Tomate", "Queso", "Albahaca"], ["almuerzo", "cena"], rating=5),
        ]

    def test_no_favorites_returns_empty(self):
        """Test that empty favorites list returns empty results"""
        sut = build_sut(self.recipes)
        result = sut.recommend_by_favorites([], None, limit=10)
        self.assertEqual(result, [])

    def test_filters_by_favorites(self):
        """Test filtering recipes by favorite ingredients"""
        sut = build_sut(self.recipes)
        result = sut.recommend_by_favorites(["pollo"], None, limit=10)
        titles = [r.title for r in result]
        self.assertIn("Pasta al Pollo", titles)

    def test_filters_by_favorites_and_category(self):
        """Test combined filtering by favorites and category"""
        sut = build_sut(self.recipes)
        result = sut.recommend_by_favorites(["tomate"], "almuerzo", limit=10)
        self.assertTrue(all("almuerzo" in [c.lower() for c in r.categories] for r in result))
        self.assertTrue(all(any("tomate" in i.lower() for i in r.ingredients) for r in result))

    def test_empty_category(self):
        """Test behavior with empty category"""
        sut = build_sut(self.recipes)
        result = sut.recommend_by_favorites(["tomate"], "", limit=10)
        self.assertTrue(all(any("tomate" in i.lower() for i in r.ingredients) for r in result))
        self.assertTrue(len(result) > 0)

    def test_invalid_favorites_type(self):
        """Test handling of invalid favorites parameter"""
        sut = build_sut(self.recipes)
        result = sut.recommend_by_favorites(None, "almuerzo", limit=10)
        self.assertEqual(result, [])

    def test_results_ordered_by_rating(self):
        """Test that results are ordered by rating"""
        sut = build_sut(self.recipes)
        result = sut.recommend_by_favorites(["tomate"], limit=10)
        ratings = [r.rating for r in result]
        self.assertEqual(ratings, sorted(ratings, reverse=True))

    def test_respects_limit(self):
        """Test that results respect the specified limit"""
        sut = build_sut(self.recipes)
        result = sut.recommend_by_favorites(["tomate"], limit=2)
        self.assertEqual(len(result), 2)

    def test_require_all_mode(self):
        """Test require_all mode for multiple ingredients"""
        sut = build_sut(self.recipes, require_all=True)
        result = sut.recommend_by_favorites(["tomate", "queso"])
        
        # Verify that each recipe contains all favorite ingredients
        for recipe in result:
            ingredients_lower = [i.lower() for i in recipe.ingredients]
            for favorite in ["tomate", "queso"]:
                favorite_lower = favorite.lower()
                # Check that the favorite ingredient is present in the recipe ingredients
                self.assertTrue(
                    any(favorite_lower in ingredient for ingredient in ingredients_lower),
                    f"La receta {recipe.title} no contiene el ingrediente favorito '{favorite}'"
                )


if __name__ == "__main__":
    unittest.main()