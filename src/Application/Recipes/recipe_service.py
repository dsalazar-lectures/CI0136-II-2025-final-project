from src.Application.Recipes.IRecipeRepository import recipe_repository

def get_all_recipes():
    return recipe_repository.get_all()

def get_recipe_by_id(recipe_id):
    return recipe_repository.get_by_id(recipe_id)