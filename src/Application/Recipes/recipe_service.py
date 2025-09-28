from src.Application.Recipes.IRecipeRepository import RecipeRepository

def get_all_recipes():
    return RecipeRepository.get_all()

def get_recipe_by_id(recipe_id):
    return RecipeRepository.get_by_id(recipe_id)