# concrete decorator
from src.Application.Recipes.RecipeFilter import RecipeFilter

class PortionsFilter(RecipeFilter):

    def __init__(self, filter_component, portions):
        super().__init__(filter_component)
        self.portions = portions

    def filter(self, recipes, portions):
        # split -
        minMaxPortions = str(portions).split('-')
        minPortion = int(minMaxPortions[0]) if len(minMaxPortions) > 0 else 0
        maxPortion = int(minMaxPortions[1]) if len(minMaxPortions) > 1 else float('inf')
        return [
            recipe for recipe in recipes
            if (minPortion <= recipe.portions and recipe.portions <= maxPortion)
        ]