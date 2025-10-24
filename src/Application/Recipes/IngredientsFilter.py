# concrete decorator
from RecipeFilter import RecipeFilter

class IngredientsFilter(RecipeFilter):

    def __init__(self, filter_component, ingredients):
        super().__init__(filter_component)
        self.ingredients = ingredients

    def filter(self, recipes, ingredients):
        matchingIngredients = []
        requestedIngredients = ingredients.split(',')
        formattedIngredients = []

        for ing in requestedIngredients:
            ing.replace("-", " ")
            formattedIngredients.append(ing)

        for recipe in recipes:
            if formattedIngredients.lower().strip in recipe.ingredients.lower():
                matchingIngredients.append(recipe)

        return matchingIngredients