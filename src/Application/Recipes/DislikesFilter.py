# concrete decorator
from src.Application.Recipes.RecipeFilter import RecipeFilter


class DislikesFilter(RecipeFilter):

    def __init__(self, filter_component, dislikes):
        super().__init__(filter_component)
        self.dislikes = [d.strip().lower() for d in dislikes]

    def filter(self, recipes):
        recipes = self._filter.filter(recipes)
        filtered = []

        for recipe in recipes:
            recipe_ingredients = [ing.strip().lower() for ing in recipe.ingredients]
            if not any(
                dislike in ingredient
                for ingredient in recipe_ingredients
                for dislike in self.dislikes
            ):
                filtered.append(recipe)

        return filtered
