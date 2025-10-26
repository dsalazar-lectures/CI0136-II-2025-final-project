# concrete decorator
from src.Application.Recipes.RecipeFilter import RecipeFilter

class CalificationFilter(RecipeFilter):

    def __init__(self, filter_component, calification):
        super().__init__(filter_component)
        self.calification = calification

    def filter(self, recipes, calification):
        return [
            recipe for recipe in recipes
            if ((recipe.califications_sumatory / recipe.califications_amount) >= calification)
        ]