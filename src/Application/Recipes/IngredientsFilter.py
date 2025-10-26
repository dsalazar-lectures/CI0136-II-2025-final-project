# concrete decorator
from src.Application.Recipes.RecipeFilter import RecipeFilter

class IngredientsFilter(RecipeFilter):

    def __init__(self, filter_component, ingredients):
        super().__init__(filter_component)
        self.ingredients = [ing.replace("-", " ").strip().lower() for ing in ingredients]

    def filter(self, recipes):
        recipes = self._filter.filter(recipes)
        matching_recipes  = []

        for recipe in recipes:
            recipe_ingredients = [ingredient.strip().lower() for ingredient in recipe.ingredients]

            if any(
                any(ing in ingredient for ingredient in recipe_ingredients)
                for ing in self.ingredients
            ):
                matching_recipes.append(recipe)
        return matching_recipes
