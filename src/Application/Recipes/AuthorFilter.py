# concrete decorator
from src.Application.Recipes.RecipeFilter import RecipeFilter

class AuthorFilter(RecipeFilter):

    def __init__(self, filter_component, author):
        super().__init__(filter_component)
        self.author = author

    def filter(self, recipes, author):
        return [
            recipe for recipe in recipes
            if (recipe.author.lower() == author.lower())
        ]