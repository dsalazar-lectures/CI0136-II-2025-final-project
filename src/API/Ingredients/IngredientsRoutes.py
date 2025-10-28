from flask import Blueprint, jsonify
from src.Application.Ingredients.IngredientUseCase import ingredient_service

ingredients_bp = Blueprint("ingredients", __name__)


@ingredients_bp.route("/ingredients", methods=["GET"])
def get_all_ingredients():
    """Get all ingredients ordered alphabetically."""
    ingredients = ingredient_service.get_all_ingredients()
    return jsonify([ingredient.to_json() for ingredient in ingredients])


@ingredients_bp.route("/ingredients/<int:ingredient_id>", methods=["GET"])
def get_ingredient_by_id(ingredient_id):
    """Get a specific ingredient by its ID."""
    ingredient = ingredient_service.get_ingredient_by_id(ingredient_id)
    if not ingredient:
        return jsonify({"error": "Ingrediente no encontrado"}), 404
    return jsonify(ingredient.to_json())


@ingredients_bp.route("/ingredients/<string:ingredient_name>", methods=["GET"])
def get_ingredient_name(ingredient_name):
    """Get a specific ingredient by its name."""
    ingredient = ingredient_service.get_ingredient_by_name(ingredient_name)
    if ingredient is None:
        return jsonify({"error": "Ingrediente no encontrado"}), 404
    return jsonify(ingredient.to_json())
