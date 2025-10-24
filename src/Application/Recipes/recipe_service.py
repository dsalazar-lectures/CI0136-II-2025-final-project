from src.Infrastructure.Recipes.CSVRecipeRepository import CSVRecipeRepository

recipe_repository = CSVRecipeRepository()

def get_all_recipes():
    return recipe_repository.get_all()

def get_recipe_by_id(recipe_id):
    return recipe_repository.get_by_id(recipe_id)

def get_recipes_by_ingredient(ingredient):
    return recipe_repository.find_by_ingredient(ingredient)

def create_recipe(recipe_data, username):
    recipe_data["author"] = username
    if not validate_data(recipe_data):
        return -1
    return recipe_repository.add_recipe(recipe_data)

def delete_recipe(recipe_id, username):
    return recipe_repository.delete_if_owned(recipe_id, username)

def update_recipe(recipe_id, updates, username):
    if not validate_data(updates):
        return -1
    return recipe_repository.update_if_owned(recipe_id, username, updates)

def validate_data(recipe_data) -> bool:
    for key, value in recipe_data.items():
        if key in ["name", "instructions"]:
            if not isinstance(value, str) or not value.strip():
                return False

        elif key in ["categories", "ingredients"]:
            if not isinstance(value, list) or len(value) == 0:
                return False
            if any(not isinstance(item, str) or not item.strip() for item in value):
                return False

        elif key in ["duration", "portions"]:
            if not isinstance(value, (int, float)):
                return False
    return True

def get_recipes_by_category(category):
    return recipe_repository.find_by_category(category)
