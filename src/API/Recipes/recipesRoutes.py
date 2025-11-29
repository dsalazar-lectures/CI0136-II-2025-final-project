from flask import Blueprint, jsonify, request
from src.Application.Recipes import recipe_service
from src.API.Recipes import recipesController
from src.Application.Profiles.Services.ProfileApplicationService import (
    ProfileApplicationService,
)
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository
from src.Application.User.Services.AuthorizationService import create_default_auth_service
from src.Model.Profiles.Roles import Role


auth_service = create_default_auth_service()

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
        return jsonify({"error": "Receta no encontrada"}), 404
    return jsonify(recipe.to_dict())


@recipes_bp.route("/recipes/<string:ingredient>", methods=["GET"])
def get_recipes_by_ingredient(ingredient):
    recipes = recipe_service.get_recipes_by_ingredient(ingredient)
    if not recipes:
        return (
            jsonify({"message": f"No se encontraron recetas con '{ingredient}'"}),
            404,
        )

    return jsonify([recipe.__str__() for recipe in recipes])


@recipes_bp.route("/addrecipe", methods=["POST"])
def create_recipe():
    is_auth, response, status_code = auth_service.is_authorized(
        request.headers,
        [Role.ADMIN, Role.GOD],
    )

    if not is_auth:
        return jsonify(response), status_code
    
    data = request.json
    status_code, response_data = recipesController.create_recipe_controller(data)
    return jsonify(response_data), status_code


@recipes_bp.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    is_auth, response, status_code = auth_service.is_authorized(
        request.headers,
        [Role.ADMIN, Role.GOD],
    )

    if not is_auth:
        return jsonify(response), status_code
    
    status_code, response_data = recipesController.delete_recipe_controller(recipe_id)
    return jsonify(response_data), status_code


@recipes_bp.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    is_auth, response, status_code = auth_service.is_authorized(
        request.headers,
        [Role.ADMIN, Role.GOD],
    )

    if not is_auth:
        return jsonify(response), status_code
    
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
            return jsonify({"error": "Duration debe ser un número"}), 400

    if "rating" in filter_criteria and filter_criteria["rating"] is not None:
        try:
            filter_criteria["rating"] = float(filter_criteria["rating"])
        except (ValueError, TypeError):
            return jsonify({"error": "Rating debe ser un número"}), 400

    filtered_recipes = recipe_service.filter_recipes(filter_criteria)

    if not filtered_recipes:
        return (
            jsonify(
                {
                    "message": "No se encontraron recetas con los filtros aplicados",
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
    is_auth, response, status_code = auth_service.is_authorized(
        request.headers,
        [Role.ADMIN, Role.GOD],
    )

    if not is_auth:
        return jsonify(response), status_code
    
    user_id = request.args.get("user_id", type=int)

    if not user_id:
        return jsonify({"error": "user_id es requerido como parámetro"}), 400

    # Get user profile
    profile = profile_service.get_profile(user_id)
    if not profile:
        return jsonify({"error": "Perfil de usuario no encontrado"}), 404

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
