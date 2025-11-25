from typing import List, Optional
from src.Application.Recipes import recipe_service
from src.Application.Menu.ICustomizedMenuService import ICustomizedMenuService
from .CustomizedMenuHandlers import (
    MenuContext,
    ExcludeIngredientsHandler,
    FavoritesFilterHandler,
    CategoryFilterHandler,
    ScoreAndSortHandler,
    LimitHandler,
)

LIMIT_OF_INGREDIENTS = 10


def _ensure_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        parts = [p.strip() for p in value.split(";")]
        return [p for p in parts if p]
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def _norm(text: str) -> str:
    return text.replace("-", " ").strip().lower()


class CustomizedMenuService(ICustomizedMenuService):
    def __init__(self, service=None, require_all: bool = False):
        self.recipe_service = service or recipe_service
        self.require_all = require_all

        # Build the chain once
        self._chain = (
            FavoritesFilterHandler()
            .set_next(CategoryFilterHandler())
            .set_next(ScoreAndSortHandler())
            .set_next(LimitHandler())
        )

        # Store reference to chain head
        self._head = ExcludeIngredientsHandler()
        self._head.set_next(FavoritesFilterHandler()).set_next(
            CategoryFilterHandler()
        ).set_next(ScoreAndSortHandler()).set_next(LimitHandler())

    def recommend_by_favorites(
        self,
        favorites: List[str] | str,
        category: Optional[str] = None,
        limit: int = LIMIT_OF_INGREDIENTS,
        excluded: List[str] | str | None = None,
    ):
        # Normalize favorite ingredients (positive filter)
        favorite_ingredients = [
            _norm(favorite)
            for favorite in _ensure_list(favorites)
            if isinstance(favorite, str) and favorite.strip()
        ]

        # Normalize ingredients to exclude (negative filter)
        excluded_ingredients = [
            _norm(ingredient)
            for ingredient in _ensure_list(excluded)
            if isinstance(ingredient, str) and ingredient.strip()
        ]

        # Get all recipes (chain will handle filtering/sorting/limit)
        all_recipes = self.recipe_service.get_all_recipes()

        ctx = MenuContext(
            favorites=favorite_ingredients,
            category=category,
            require_all=self.require_all,
            limit=limit,
            excluded_ingredients=excluded_ingredients,
        )

        return self._head.run(all_recipes, ctx)
