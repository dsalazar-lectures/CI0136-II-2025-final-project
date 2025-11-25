from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Any


def _norm(text: str) -> str:
    return text.replace("-", " ").strip().lower()


@dataclass
class MenuContext:
    favorites: List[str]
    limit: int
    category: Optional[str] = None
    require_all: bool = False  # True (AND), False (OR)
    excluded_ingredients: Optional[List[str]] = None

    def category_norm(self) -> Optional[str]:
        return (
            _norm(self.category)
            if isinstance(self.category, str) and self.category
            else None
        )


class MenuHandler(ABC):
    _next: Optional[MenuHandler] = None

    def set_next(self, next_handler: MenuHandler) -> MenuHandler:
        self._next = next_handler
        return next_handler

    def run(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        processed = self.handle(recipes, ctx)
        if self._next:
            return self._next.run(processed, ctx)
        return processed

    @abstractmethod
    def handle(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        pass

class ExcludeIngredientsHandler(MenuHandler):
    """Filter out any recipes that contain excluded ingredients."""

    def handle(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        excluded = [
            _norm(ingredient)
            for ingredient in (ctx.excluded_ingredients or [])
            if isinstance(ingredient, str) and ingredient.strip()
        ]
        if not excluded:
            return recipes

        def is_safe(recipe) -> bool:
            recipe_ingredients = [
                _norm(ingredient)
                for ingredient in getattr(recipe, "ingredients", [])
                if isinstance(ingredient, str)
            ]
            # Recipe is safe if NONE of the excluded strings appear
            return not any(
                excl in ingredient
                for excl in excluded
                for ingredient in recipe_ingredients
            )

        return [recipe for recipe in recipes if is_safe(recipe)]

class FavoritesFilterHandler(MenuHandler):
    def handle(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        favorite_ingredients = ctx.favorites
        if not favorite_ingredients:
            # If no favorites provided, return empty list
            return []

        def has_match(recipe) -> bool:
            recipe_ingredients = [
                _norm(ingredient)
                for ingredient in getattr(recipe, "ingredients", [])
                if isinstance(ingredient, str)
            ]
            if ctx.require_all:
                # AND: recipe must contain ALL favorite ingredients (as substrings)
                return all(
                    any(favorite in ingredient for ingredient in recipe_ingredients)
                    for favorite in favorite_ingredients
                )
            # OR: recipe must contain at least one favorite ingredient
            return any(
                any(favorite in ingredient for ingredient in recipe_ingredients)
                for favorite in favorite_ingredients
            )

        return [recipe for recipe in recipes if has_match(recipe)]


class CategoryFilterHandler(MenuHandler):
    def handle(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        category_normalized = ctx.category_norm()
        if not category_normalized:
            return recipes

        def in_category(recipe) -> bool:
            recipe_categories = [
                _norm(category) for category in getattr(recipe, "categories", [])
            ]
            # Exact match per category (matches behavior of CategoryFilter)
            return any(
                category == category_normalized for category in recipe_categories
            )

        return [recipe for recipe in recipes if in_category(recipe)]


class ScoreAndSortHandler(MenuHandler):
    def handle(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        favorite_ingredients = ctx.favorites

        def score(recipe) -> int:
            recipe_ingredients = [
                _norm(ingredient)
                for ingredient in getattr(recipe, "ingredients", [])
                if isinstance(ingredient, str)
            ]
            return sum(
                1
                for favorite in favorite_ingredients
                if any(favorite in ingredient for ingredient in recipe_ingredients)
            )

        # Tiebreakers: first by rating (desc), then by title (asc) if exists
        return sorted(
            recipes,
            key=lambda recipe: (
                -score(recipe),
                -getattr(recipe, "rating", 0),
                getattr(recipe, "title", ""),
            ),
        )


class LimitHandler(MenuHandler):
    def handle(self, recipes: List[Any], ctx: MenuContext) -> List[Any]:
        return recipes[: max(ctx.limit, 0)]
