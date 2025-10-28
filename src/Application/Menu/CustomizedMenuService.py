from typing import List, Optional
from src.Application.Recipes import recipe_service
from src.Application.Menu.ICustomizedMenuService import ICustomizedMenuService
from .CustomizedMenuHandlers import (
    MenuContext,
    FavoritesFilterHandler,
    CategoryFilterHandler,
    ScoreAndSortHandler,
    LimitHandler,
)

LIMIT_OF_INGREDIENTS = 10

def _ensure_list(value):
    if isinstance(value, str):
        return [item.strip() for item in value.split(";") if item.strip()]
    return value or []

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
        self._head = FavoritesFilterHandler()
        self._head.set_next(CategoryFilterHandler()).set_next(ScoreAndSortHandler()).set_next(LimitHandler())

    def recommend_by_favorites(
        self,
        favorites: List[str] | str,
        category: Optional[str] = None,
        limit: int = LIMIT_OF_INGREDIENTS
    ):
        # Normalize favorite ingredients
        favorite_ingredients = [_norm(favorite) for favorite in _ensure_list(favorites) if isinstance(favorite, str) and favorite.strip()]

        # Get all recipes (chain will handle filtering/sorting/limit)
        all_recipes = self.recipe_service.get_all_recipes()

        ctx = MenuContext(
            favorites=favorite_ingredients,
            category=category,
            require_all=self.require_all,
            limit=limit,
        )

        return self._head.run(all_recipes, ctx)
