from flask import Blueprint, jsonify, request
from src.Application.Recipes import recipe_service

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

    allowed_fields = {"name", "categories", "ingredients", "duration", "instructions", "portions"}
    safe_updates = {k: v for k, v in updates.items() if k in allowed_fields}

    result = recipe_service.update_recipe(recipe_id, safe_updates, username)
    if result == -1:
        return jsonify({"error": "Datos de actualización inválidos"}), 400
    if result is None:
        return jsonify({"error": "Receta no encontrada"}), 404
    if result is False:
        return jsonify({"error": "No autorizado para editar esta receta"}), 403
    return jsonify(result.to_dict())
