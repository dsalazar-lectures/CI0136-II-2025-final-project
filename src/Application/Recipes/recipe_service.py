import random
from src.Infrastructure.Recipes.CSVRecipeRepository import CSVRecipeRepository
from src.Application.Recipes.FilterComposer import FilterComposer
from src.Shared.Logs.custom_logger import CustomLogger

recipe_repository = CSVRecipeRepository()
filter_composer = FilterComposer()
logger = CustomLogger()


def get_all_recipes():
    return recipe_repository.get_all()


def get_recipe_by_id(recipe_id):
    return recipe_repository.get_by_id(recipe_id)


def get_recipes_by_ingredient(ingredient):
    return recipe_repository.find_by_ingredient(ingredient)


def create_recipe(recipe_data, username):
    recipe_data["author"] = username
    if not validate_create_data(recipe_data):
        logger.log(
            level="error",
            user=username,
            role="-",  # Can be changed if necessary
            action="Create recipe",
            id_object="-",
            description=f"Validation error by {username}",
        )
        return -1
    recipe = recipe_repository.add_recipe(recipe_data)

    if recipe is None:
        logger.log(
            level="error",
            user=username,
            role="-",
            action="Create recipe",
            id_object="-",
            description=f"Failed to create recipe {username}",
        )
        return -1
    else:
        logger.log(
            level="info",
            user=username,
            role="-",
            action="Create recipe",
            id_object=recipe.id,
            description=f"Recipe '{recipe.name}' created successfully by {username}",
        )
        return recipe


def delete_recipe(recipe_id, username):
    recipe = recipe_repository.delete_if_owned(recipe_id, username)

    if recipe is None:
        logger.log(
            level="error",
            user=username,
            role="-",
            action="Delete recipe",
            id_object="-",
            description=f"Recipe {recipe_id} not found",
        )
        return -1
    elif recipe is False:
        logger.log(
            level="warning",
            user=username,
            role="-",
            action="Delete recipe",
            id_object=recipe_id,
            description=f"User {username} does not own recipe {recipe_id}",
        )
        return 0
    else:
        logger.log(
            level="info",
            user=username,
            role="-",
            action="Delete recipe",
            id_object=recipe_id,
            description=f"Recipe {recipe_id} deleted successfully",
        )
        return recipe


def update_recipe(recipe_id, updates, username):
    if not validate_data(updates):
        logger.log(
            level="error",
            user=username,
            role="-",
            action="Update recipe",
            id_object=recipe_id,
            description=f"Validation failed for update data in recipe {recipe_id}",
        )
        return -1
    recipe = recipe_repository.update_if_owned(recipe_id, username, updates)

    if recipe is None:
        logger.log(
            level="error",
            user=username,
            role="-",
            action="Update recipe",
            id_object=recipe_id,
            description=f"Recipe {recipe_id} not found",
        )
        return -1
    elif recipe is False:
        logger.log(
            level="warning",
            user=username,
            role="-",
            action="Update recipe",
            id_object=recipe_id,
            description=f"User {username} does not own recipe {recipe_id}",
        )
        return 0
    else:
        logger.log(
            level="info",
            user=username,
            role="-",
            action="Update recipe",
            id_object=recipe_id,
            description=f"Recipe {recipe_id} updated successfully by {username})",
        )
        return recipe


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
        "name",
        "categories",
        "ingredients",
        "duration",
        "instructions",
        "portions",
        "author",
    ]

    for field in required_fields:
        if field not in recipe_data:
            return False

    return validate_data(recipe_data)


def get_recipes_by_category(category):
    return recipe_repository.find_by_category(category)


def get_random_recipe_by_category(category):
    recipes = recipe_repository.find_by_category(category)
    if not recipes:
        return None

    return random.choice(recipes)
