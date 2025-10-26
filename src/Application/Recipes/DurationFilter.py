# concrete decorator
from src.Application.Recipes.RecipeFilter import RecipeFilter


class DurationFilter(RecipeFilter):

    def __init__(self, filter_component, duration):
        super().__init__(filter_component)
        self.duration = duration

    def filter(self, recipes):
        recipes = self._filter.filter(recipes)
        return [recipe for recipe in recipes if recipe.duration <= self.duration]
