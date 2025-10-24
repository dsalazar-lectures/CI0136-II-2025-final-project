from RecipeFilter import RecipeFilter

class CategoryFilter(RecipeFilter):

    def __init__(self, filter_component, categories):
        super().__init__(filter_component)
        self.categories = categories

    def filter(self, recipes, category):
        return [
            recipe for recipe in recipes
            if (recipe.categories.lower() == category.lower())
        ]