from src.Application.Recipes.RecipeFilter import RecipeFilter


class CategoryFilter(RecipeFilter):

    def __init__(self, filter_component, categories):
        super().__init__(filter_component)
        self.categories = [cat.strip().lower() for cat in categories]

    def filter(self, recipes):
        recipes = self._filter.filter(recipes)
        filtered = []
        for recipe in recipes:
            recipe_categories = [
                category.strip().lower() for category in recipe.categories
            ]
            if any(category in recipe_categories for category in self.categories):
                filtered.append(recipe)

        return filtered
