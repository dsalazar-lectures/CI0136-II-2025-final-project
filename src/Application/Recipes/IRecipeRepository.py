from src.Database.Recipes.RecipesSchema import system_recipes

class RecipeRepository:
    def get_all(self):
        return system_recipes

    def get_by_id(self, recipe_id):
        return next((recipe for recipe in system_recipes if recipe.id == recipe_id), None)

recipe_repository = RecipeRepository()
