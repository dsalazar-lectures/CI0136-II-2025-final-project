from flask import Blueprint, jsonify, request
from src.Application.Recipes import recipe_service
from src.API.Recipes import recipesController
from src.Application.Profiles.Services.ProfileApplicationService import (
    ProfileApplicationService,
)
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository

recipes_bp = Blueprint("recipes", __name__)
profile_service = ProfileApplicationService(ProfileRepository("profiles.csv"))


@recipes_bp.route("/recipes", methods=["GET"])
def get_all_recipes():
    recipes = recipe_service.get_all_recipes()
    return jsonify([recipe.__str__() for recipe in recipes])


@recipes_bp.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    recipe = recipe_service.get_recipe_by_id(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    return jsonify(recipe.to_dict())


@recipes_bp.route("/recipes/<string:ingredient>", methods=["GET"])
def get_recipes_by_ingredient(ingredient):
    recipes = recipe_service.get_recipes_by_ingredient(ingredient)
    if not recipes:
        return (
            jsonify({"message": f"Could not find recipes with '{ingredient}'"}),
            404,
        )

    return jsonify([recipe.__str__() for recipe in recipes])


@recipes_bp.route("/addrecipe", methods=["POST"])
def create_recipe():
    data = request.json
    status_code, response_data = recipesController.create_recipe_controller(data)
    return jsonify(response_data), status_code


@recipes_bp.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    status_code, response_data = recipesController.delete_recipe_controller(recipe_id)
    return jsonify(response_data), status_code


@recipes_bp.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    updates = request.json or {}
    status_code, response_data = recipesController.update_recipe_controller(
        recipe_id, updates
    )
    return jsonify(response_data), status_code


@recipes_bp.route("/recipes/filter", methods=["POST"])
def filter_recipes():
    filter_criteria = request.json or {}

    # Validate and convert types if needed
    if "duration" in filter_criteria and filter_criteria["duration"] is not None:
        try:
            filter_criteria["duration"] = int(filter_criteria["duration"])
        except (ValueError, TypeError):
            return jsonify({"error": "Duration must be a number"}), 400

    if "rating" in filter_criteria and filter_criteria["rating"] is not None:
        try:
            filter_criteria["rating"] = float(filter_criteria["rating"])
        except (ValueError, TypeError):
            return jsonify({"error": "Rating must be a number"}), 400

    filtered_recipes = recipe_service.filter_recipes(filter_criteria)

    if filtered_recipes == -1:
        return (
            jsonify({"message": "Invalid data"}),
            400,
        )

    if not filtered_recipes:
        return (
            jsonify(
                {
                    "message": "Could not find recipes with selected filters",
                    "recipes": [],
                }
            ),
            200,
        )

    return (
        jsonify(
            {
                "count": len(filtered_recipes),
                "recipes": [recipe.to_dict() for recipe in filtered_recipes],
            }
        ),
        200,
    )


@recipes_bp.route("/recipes/prioritized", methods=["GET"])
def get_prioritized_recipes():
    """
    Get all recipes prioritized by user's favorite ingredients.
    """
    user_id = request.args.get("user_id", type=int)

    if not user_id:
        return jsonify({"error": "user_id is required as parameter"}), 400

    # Get user profile
    profile = profile_service.get_profile(user_id)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    # Get prioritized recipes based on user's favorite foods
    prioritized_recipes = recipe_service.get_prioritized_recipes(profile.favorite_foods)

    return (
        jsonify(
            {
                "count": len(prioritized_recipes),
                "user_id": user_id,
                "favorite_ingredients": profile.favorite_foods,
                "recipes": [recipe.to_dict() for recipe in prioritized_recipes],
            }
        ),
        200,
    )


@recipes_bp.route("/recipes/<int:recipe_id>/rate", methods=["POST"])
def rate_recipe(recipe_id):
    data = request.json or {}
    status_code, response_data = recipesController.rate_recipe_controller(
        recipe_id, data
    )
    return jsonify(response_data), status_code
