from src.Database.Recipes.RecipesSchema import system_recipes

def get_all_recipes():
    return system_recipes

def get_recipe_by_id(recipe_id):
    recipes = get_all_recipes()
    return next((recipe for recipe in recipes if recipe.id == recipe_id), None)
