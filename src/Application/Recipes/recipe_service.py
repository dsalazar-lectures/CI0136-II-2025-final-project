from src.Application.Recipes.IRecipeRepository import recipe_repository

def get_all_recipes():
    return recipe_repository.get_all()

def get_recipe_by_id(recipe_id):
    return recipe_repository.get_by_id(recipe_id)

def get_recipes_by_ingredient(ingredient):
    return recipe_repository.find_by_ingredient(ingredient)

def create_recipe(recipe_data, username):
    recipe_data["author"] = username
    return recipe_repository.add_recipe(recipe_data)

def delete_recipe(recipe_id, username):
    return recipe_repository.delete_if_owned(recipe_id, username)