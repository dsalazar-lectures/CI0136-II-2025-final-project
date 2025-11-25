from typing import List, Optional


class FakeRecipe:
    """Mock recipe class for tests in Menu customized service"""

    def __init__(
        self,
        title: str,
        ingredients: List[str],
        categories: Optional[List[str]] = None,
        rating: int = 0,
        id: int | None = None,
    ):
        self.id = id
        self.title = title
        self.ingredients = ingredients
        self.categories = categories or []
        self.rating = rating


class FakeRecipeService:
    """Simple fake recipe service used by unit tests"""

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
