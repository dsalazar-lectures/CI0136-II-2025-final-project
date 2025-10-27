from typing import List, Optional
from src.Application.Recipes import recipe_service
from .CustomizedMenuHandlers import (
    MenuContext,
    FavoritesFilterHandler,
    CategoryFilterHandler,
    ScoreAndSortHandler,
    LimitHandler,
)

LIMIT_OF_INGREDIENTS = 10

def _ensure_list(val):
    if isinstance(val, str):
        return [x.strip() for x in val.split(";") if x.strip()]
    return val or []

def _norm(s: str) -> str:
    return s.replace("-", " ").strip().lower()

class CustomizedMenuService:
    def __init__(self, service=None, require_all: bool = False):
        self.recipe_service = service or recipe_service
        self.require_all = require_all

        # Construye la cadena una vez
        self._chain = (
            FavoritesFilterHandler()
                .set_next(CategoryFilterHandler())
                .set_next(ScoreAndSortHandler())
                .set_next(LimitHandler())
        )

        # Guarda referencia a la cabeza de la cadena
        self._head = FavoritesFilterHandler()
        self._head.set_next(CategoryFilterHandler()).set_next(ScoreAndSortHandler()).set_next(LimitHandler())

    def recommend_by_favorites(
        self,
        favorites: List[str] | str,
        limit: int = LIMIT_OF_INGREDIENTS,
        category: Optional[str] = None,
    ):
        # Normaliza favoritos
        favs = [_norm(f) for f in _ensure_list(favorites) if isinstance(f, str) and f.strip()]

        # Trae todas las recetas (la cadena se encargará del filtrado/orden/limit)
        all_recipes = self.recipe_service.get_all_recipes()

        ctx = MenuContext(
            favorites=favs,
            category=category,
            require_all=self.require_all,
            limit=limit,
        )

        return self._head.run(all_recipes, ctx)
