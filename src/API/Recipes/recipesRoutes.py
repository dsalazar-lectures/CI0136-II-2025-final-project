from flask import Blueprint, jsonify, request
from src.Application.Recipes import recipe_service

recipes_bp = Blueprint("recipes", __name__)

@recipes_bp.route("/recipes", methods=["GET"])
def get_all_recipes():
    recipes = recipe_service.get_all_recipes()
    return jsonify([recipe.to_dict() for recipe in recipes])

@recipes_bp.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id):
    recipe = recipe_service.get_recipe_by_id(recipe_id)
    if not recipe:
        return jsonify({"error": "Receta no encontrada"}), 404
    return jsonify(recipe.to_dict())

@recipes_bp.route("/recipes", methods=["POST"])
def create_recipe():
    data = request.json
    required_fields = ["name", "categories", "ingredients", "duration", "instructions", "portions"]
    username = "myUser"

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Se necesita información adicional sobre la receta"}), 400

    recipe = recipe_service.create_recipe(data, username)
    return jsonify(recipe.to_dict()), 201