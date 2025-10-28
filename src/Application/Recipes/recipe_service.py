import random
from src.Infrastructure.Recipes.CSVRecipeRepository import CSVRecipeRepository
from src.Application.Recipes.FilterComposer import FilterComposer

recipe_repository = CSVRecipeRepository()
filter_composer = FilterComposer()


def get_all_recipes():
    return recipe_repository.get_all()


def get_recipe_by_id(recipe_id):
    return recipe_repository.get_by_id(recipe_id)


def get_recipes_by_ingredient(ingredient):
    return recipe_repository.find_by_ingredient(ingredient)


def create_recipe(recipe_data, username):
    recipe_data["author"] = username
    if not validate_create_data(recipe_data):
        return -1
    return recipe_repository.add_recipe(recipe_data)


def delete_recipe(recipe_id, username):
    return recipe_repository.delete_if_owned(recipe_id, username)


def update_recipe(recipe_id, updates, username):
    if not validate_data(updates):
        return -1
    return recipe_repository.update_if_owned(recipe_id, username, updates)


def filter_recipes(filter_criteria):
    all_recipes = recipe_repository.get_all()
    return filter_composer.apply_filters(all_recipes, filter_criteria)


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

def validate_create_data(recipe_data) -> bool:
    required_fields = [
        "name", "categories", "ingredients",
        "duration", "instructions", "portions", "author"
    ]

    for field in required_fields:
        if field not in recipe_data:
            return False
        
    return validate_data(recipe_data)


def get_random_recipe_by_category(category):
    recipes = recipe_repository.find_by_category(category)
    if not recipes:
        return None

    return random.choice(recipes)
