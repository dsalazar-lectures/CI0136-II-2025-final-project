# concrete decorator
from src.Application.Recipes.RecipeFilter import RecipeFilter

class DurationFilter(RecipeFilter):

    def __init__(self, filter_component, duration):
        super().__init__(filter_component)
        self.duration = duration

    def filter(self, recipes, duration):
        return [
            recipe for recipe in recipes
            if (recipe.duration <= duration)
        ]