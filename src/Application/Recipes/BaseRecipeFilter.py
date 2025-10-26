# concrete component in Decorator pattern
from src.Application.Recipes.IFilter import IFilter


class BaseRecipeFilter(IFilter):
    """Base filter that returns all recipes without filtering"""

    def filter(self, recipes):
        return recipes
