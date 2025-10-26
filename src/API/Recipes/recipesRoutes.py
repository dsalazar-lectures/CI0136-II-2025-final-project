from flask import Blueprint, jsonify, request
from src.Application.Recipes import recipe_service
from src.API.Recipes.recipesController import update_recipe_controller

recipes_bp = Blueprint("recipes", __name__)


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
        return jsonify({"message": f"No se encontraron recetas con '{ingredient}'"}), 404
    
    return jsonify([recipe.__str__() for recipe in recipes])


@recipes_bp.route("/addrecipe", methods=["POST"])
def create_recipe():
    data = request.json
    username = "myUser"
    recipe = recipe_service.create_recipe(data, username)
    if recipe == -1:
        return jsonify({"error": "Se necesita información adicional sobre la receta"}), 400
    return jsonify(recipe.to_dict())


@recipes_bp.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    username = "myUser"  # Change later to actual username
    result = recipe_service.delete_recipe(recipe_id, username)
    if result is None:
        return jsonify({"error": "Receta no encontrada"}), 404
    if result is False:
        return jsonify({"error": "No autorizado para eliminar esta receta"}), 403
    return jsonify({"message": "Receta eliminada", "recipe": result.__str__()})


@recipes_bp.route("/recipes/<int:recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    username = "myUser"  # Change later to actual username
    updates = request.json or {}
    status_code, response_data = update_recipe_controller(recipe_id, updates, username)
    return jsonify(response_data), status_code

@recipes_bp.route("/recipes/filter", methods=["POST"])
def filter_recipes():
    filter_criteria = request.json or {}
    
    # Validate and convert types if needed
    if 'duration' in filter_criteria and filter_criteria['duration'] is not None:
        try:
            filter_criteria['duration'] = int(filter_criteria['duration'])
        except (ValueError, TypeError):
            return jsonify({"error": "Duration debe ser un número"}), 400
    
    if 'rating' in filter_criteria and filter_criteria['rating'] is not None:
        try:
            filter_criteria['rating'] = float(filter_criteria['rating'])
        except (ValueError, TypeError):
            return jsonify({"error": "Rating debe ser un número"}), 400
    
    filtered_recipes = recipe_service.filter_recipes(filter_criteria)
    
    if not filtered_recipes:
        return jsonify({"message": "No se encontraron recetas con los filtros aplicados", "recipes": []}), 200
    
    return jsonify({
        "count": len(filtered_recipes),
        "recipes": [recipe.to_dict() for recipe in filtered_recipes]
    }), 200