from typing import List
from src.Model.Recipes.Recipes import Recipe


class RecipePrioritizer:
    @staticmethod
    def _normalize(text: str) -> str:
        """
        Normalize text for comparison: lowercase and replace hyphens with spaces.
        """
        if not isinstance(text, str):
            return ""
        return text.replace("-", " ").strip().lower()

    def _score_recipe(self, recipe: Recipe, favorite_ingredients: List[str]) -> int:
        """
        Calculate score for a recipe based on how many favorite ingredients it contains.
        """
        if not hasattr(recipe, "ingredients") or not recipe.ingredients:
            return 0

        # Normalize recipe ingredients
        recipe_ingredients = [
            self._normalize(ingredient)
            for ingredient in recipe.ingredients
            if isinstance(ingredient, str)
        ]

        # Count matches (substring matching)
        score = 0
        for favorite in favorite_ingredients:
            if any(favorite in ingredient for ingredient in recipe_ingredients):
                score += 1

        return score

    def prioritize(self, recipes: List[Recipe], favorite_foods: List[str]) -> List[Recipe]:
        """
        Recipes with more favorite ingredients appear first.
        Recipes without any favorite ingredients appear last
        """
        if not recipes:
            return []

        if not favorite_foods:
            # No favorites provided, return original order
            return recipes

        # Normalize favorite ingredients
        favorite_ingredients = [
            self._normalize(food)
            for food in favorite_foods
            if isinstance(food, str) and food.strip()
        ]

        if not favorite_ingredients:
            return recipes

        def get_score(recipe):
            """Calculate score for a single recipe"""
            return self._score_recipe(recipe, favorite_ingredients)

        # Sort by score (descending), stable sort preserves original order for ties
        return sorted(recipes, key=get_score, reverse=True)