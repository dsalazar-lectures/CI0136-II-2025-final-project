# decorator interface
from src.Application.Recipes.IFilter import IFilter

class RecipeFilter(IFilter):

    def __init__(self, filter_component: IFilter):
        self._filter = filter_component

    def filter(self, recipes):
        return self._filter.filter(recipes)