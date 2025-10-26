from flask import Blueprint, jsonify, request
from src.Application.Recipes import recipe_service
from src.Application.Menu import menu_service

menu_bp = Blueprint("menu", __name__)


@menu_bp.route("/menu", methods=["GET"])
def get_menu():
    category = request.args.get("category")
    recipes = recipe_service.get_recipes_by_category(category)
    limited_recipes = recipes[:5]
    return jsonify([recipe.to_dict() for recipe in limited_recipes])


@menu_bp.route("/menu/<string:category>/<int:count>", methods=["GET"])
def get_menus_number(category: str, count: int):
    """Generate N menus for a given category using path parameters.
    Example: GET /api/menu/almuerzo/5
    """
    # Validate count
    if count < 1:
        return jsonify({"error": "el número de menús a generar debe ser un número entero positivo"}), 400
    # Category comes from the path; simply fetch recipes
    recipes = recipe_service.get_recipes_by_category(category)
    if not recipes:
        return jsonify({"message": f"No se encontraron recetas en la categoría '{category}'"}), 404
    # Generate menus
    menus = menu_service.generate_menus(recipes, count)
    return jsonify(menus)
