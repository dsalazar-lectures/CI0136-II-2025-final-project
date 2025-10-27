from typing import List, Optional
from src.Application.Recipes import recipe_service

def _ensure_list(val):
    # Convert input to a list of strings
    if isinstance(val, str):
        return [x.strip() for x in val.split(";") if x.strip()]
    return val or []

def _norm(s: str) -> str:
    return s.replace("-", " ").strip().lower()

class CustomizedMenuService:
    def __init__(self, service=None):
        self.recipe_service = service or recipe_service

    def recommend_by_favorites(
        self,
        favorites: List[str] | str,
        category: Optional[str] = None,
        limit: int = 10,
    ):
        favs = [_norm(f) for f in _ensure_list(favorites) if isinstance(f, str) and f.strip()]

        # If no favorites provided, return empty list
        if not favs:
            return []

        # 1) Get ALL recipes and filter by favorites (at least 1 match required)
        all_recipes = self.recipe_service.get_all_recipes()

        def has_match(recipe) -> bool:
            ings = [_norm(i) for i in getattr(recipe, "ingredients", []) if isinstance(i, str)]
            return any(any(f in ing for ing in ings) for f in favs)

        fav_filtered = [r for r in all_recipes if has_match(r)]

        # 2) If category provided, apply category filter (using normalized values)
        result = fav_filtered
        if category:
            cat_norm = _norm(category)
            def in_category(recipe) -> bool:
                rc_list = [ _norm(c) for c in getattr(recipe, "categories", []) ]
                return any(cat_norm == rc for rc in rc_list)
            result = [r for r in fav_filtered if in_category(r)]

        # 3) Sort by number of favorite ingredients matches
        def score(recipe):
            ings = [_norm(i) for i in getattr(recipe, "ingredients", []) if isinstance(i, str)]
            return sum(1 for f in favs if any(f in ing for ing in ings))
        result.sort(key=score, reverse=True)

        return result[:limit]
    