from src.Application.Recipes.RecipeFilter import RecipeFilter

class CategoryFilter(RecipeFilter):

    def __init__(self, filter_component, categories):
        super().__init__(filter_component)
        self.categories = categories

    def filter(self, recipes, category):
        category_lower = category.lower()
        return [
            recipe for recipe in recipes
            if any(cat.lower() == category_lower for cat in recipe.categories)
        ]