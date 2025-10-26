from src.Application.Recipes.RecipeFilter import RecipeFilter

class CategoryFilter(RecipeFilter):

    def __init__(self, filter_component, categories):
        super().__init__(filter_component)
        self.categories = categories

    def filter(self, recipes):
        recipes = self._filter.filter(recipes)
        category_lower = self.categories.lower()
        return [
            recipe for recipe in recipes
            if any(cat.lower() == category_lower for cat in recipe.categories)
        ]