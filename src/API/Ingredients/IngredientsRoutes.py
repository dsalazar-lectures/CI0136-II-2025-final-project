from flask import Blueprint, jsonify, request
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


@ingredients_bp.route("/ingredients/create", methods=["POST"])
def create_new_ingredient():
    """Create a new ingredient"""
    name = request.json.get("name")
    if not name:
        return jsonify({"error": "Ingredient name is required"}), 404
    categories = request.json.get("categories")
    substitutes = request.json.get("substitutes")
    components = request.json.get("components")

    ingredient_service.create_ingredient(name, categories, substitutes, components)

    return jsonify({"message": "Ingredient created successfully"}), 201


@ingredients_bp.route("/ingredients/update", methods=["POST"])
def update_ingredient():
    """Update one or more fields of an ingredient"""
    id = request.json.get("id")
    ingredient = ingredient_service.get_ingredient_by_id(id)
    if ingredient is None:
        return jsonify({"message": "Ingredient not found"}), 404

    data = request.json

    for field in ["categories", "substitutes", "components"]:
        if field in data and not isinstance(data[field], list):
            return jsonify({"error": f"{field} must be a list"}), 400

    if "categories" in request.json:
        ingredient_service.update_categories(id, data["categories"])

    if "substitutes" in request.json:
        ingredient_service.update_substitutes(id, data["substitutes"])

    if "components" in request.json:
        ingredient_service.update_components(id, data["components"])

    return jsonify({"message": "Ingredient updated successfully"}), 200


@ingredients_bp.route("/ingredients/delete", methods=["POST"])
def delete_ingredient():
    """Delete an ingredient"""
    # User permissions need to be validated here
    id = request.json.get("id")

    result = ingredient_service.delete_ingredient(id)

    if result == "ID is not valid":
        return jsonify({"error": "Ingredient not found"}), 404

    return jsonify({"message": "Ingredient deleted successfully"}), 200
