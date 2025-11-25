from flask import request
from src.Application.Recipes import recipe_service
from src.Infrastructure.User.UserRepository import UserRepository

user_repository = UserRepository()


def get_username_from_request():
    user_id = request.args.get("user_id", type=int)

    if not user_id:
        return None
    
    user = user_repository.get_user_by_id(user_id)
    if not user:
        return None

    return user.username


def create_recipe_controller(data):
    username = get_username_from_request()

    if not username:
        return 401, {
            "error": "Invalid user_id"
        }

    recipe = recipe_service.create_recipe(data, username)

    if recipe == -1:
        return 400, {"error": "Additional recipe information is required"}

    return 201, {"message": "Recipe successfully created", "recipe": recipe.to_dict()}


def delete_recipe_controller(recipe_id):
    username = get_username_from_request()

    if not username:
        return 401, {
            "error": "Invalid user_id"
        }

    result = recipe_service.delete_recipe(recipe_id, username)

    if result is None:
        return 404, {"error": "Recipe not found"}

    if result is False:
        return 403, {"error": "Not authorized to delete this recipe"}

    return 200, {"message": "Recipe successfully deleted", "recipe": result.__str__()}


def update_recipe_controller(recipe_id, updates):
    username = get_username_from_request()

    if not username:
        return 401, {
            "error": "Invalid user_id"
        }

    allowed_fields = {
        "name",
        "categories",
        "ingredients",
        "duration",
        "instructions",
        "portions",
    }
    safe_updates = {k: v for k, v in updates.items() if k in allowed_fields}

    result = recipe_service.update_recipe(recipe_id, safe_updates, username)

    if result == -1:
        return 400, {"error": "Invalid update data"}
    if result is None:
        return 404, {"error": "Recipe not found"}
    if result is False:
        return 403, {"error": "Not authorized to edit this recipe"}

    return 200, result.to_dict()

def rate_recipe_controller(recipe_id, data):
    username = get_username_from_request()

    if not username:
        return 401, {"error": "Invalid user_id"}

    if "rating" not in data:
        return 400, {"error": "'rating' is required (1 to 5)"}

    result = recipe_service.rate_recipe(recipe_id, username, data["rating"])

    if result is None:
        return 404, {"error": "Recipe not found"}

    if result is False:
        return 403, {"error": "You have already rated this recipe"}

    if result == -1:
        return 400, {"error": "Invalid rating value (must be between 1 and 5)"}

    return 200, {"message": "Rating submitted successfully", "recipe": result.to_dict()}

