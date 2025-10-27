from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Any

def _norm(s: str) -> str:
    return s.replace("-", " ").strip().lower()

@dataclass
class MenuContext:
    favorites: List[str]            
    limit: int
    category: Optional[str] = None
    require_all: bool = False # AND (True) vs OR (False)

    def category_norm(self) -> Optional[str]:
        return _norm(self.category) if isinstance(self.category, str) and self.category else None

class MenuHandler(ABC):
    _next: Optional[MenuHandler] = None

    def set_next(self, nxt: MenuHandler) -> MenuHandler:
        self._next = nxt
        return nxt

    def run(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        processed = self.handle(recipes, ctx)
        if self._next:
            return self._next.run(processed, ctx)
        return processed

    @abstractmethod
    def handle(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        pass

class FavoritesFilterHandler(MenuHandler):
    def handle(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        favs = ctx.favorites
        if not favs:
            # Regla de negocio: sin favoritos, no devolvemos nada
            return []

        def has_match(recipe) -> bool:
            ings = [_norm(i) for i in getattr(recipe, "ingredients", []) if isinstance(i, str)]
            if ctx.require_all:
                # AND: todos los favoritos deben aparecer (como substring) en algún ingrediente
                return all(any(f in ing for ing in ings) for f in favs)
            # OR: al menos uno
            return any(any(f in ing for ing in ings) for f in favs)

        return [r for r in recipes if has_match(r)]

class CategoryFilterHandler(MenuHandler):
    def handle(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        cat = ctx.category_norm()
        if not cat:
            return recipes
        def in_category(recipe) -> bool:
            cats = [_norm(c) for c in getattr(recipe, "categories", [])]
            # Igualdad exacta por elemento (coincide con tu CategoryFilter actual)
            return any(c == cat for c in cats)
        return [r for r in recipes if in_category(r)]

class ScoreAndSortHandler(MenuHandler):
    def handle(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        favs = ctx.favorites
        def score(recipe) -> int:
            ings = [_norm(i) for i in getattr(recipe, "ingredients", []) if isinstance(i, str)]
            return sum(1 for f in favs if any(f in ing for ing in ings))
        # Desempate: rating desc, luego título asc si existe
        return sorted(
            recipes,
            key=lambda r: (-score(r), -getattr(r, "rating", 0), getattr(r, "title", "")),
        )

class LimitHandler(MenuHandler):
    def handle(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        return recipes[: max(ctx.limit, 0)]
