from flask import Blueprint, jsonify, request
from src.Application.Recipes import recipe_service

recipes_bp = Blueprint("menu", __name__)

@recipes_bp.route("/menu", methods=["GET"])
def get_menu():
    category = request.args.get("category")
    recipes = recipe_service.get_recipes_by_category(category)
    limited_recipes = recipes[:5]
    return jsonify([recipe.to_dict() for recipe in limited_recipes])

@recipes_bp.route("/menu/<string:category>/<int:count>", methods=["GET"])
def generate_menus(category: str, count: int):
    """Generate N menus for a given category using path parameters.
    Example: GET /api/menu/almuerzo/5
    """
    # Validate count
    if count < 1:
        return jsonify({"error": "el número de menús a generar debe ser un número entero positivo"}), 400
    # Category comes from the path; simply fetch recipes
    recipes = recipe_service.get_recipes_by_category(category)
    if not recipes:
        return jsonify([])
    # Generate menus
    menus = []
    n_recipes = len(recipes)
    for i in range(1, count + 1):
        recipe = recipes[(i - 1) % n_recipes]
        menus.append({
            "menu": f"Menú #{i}",
            "recipe": recipe.to_dict(),
        })
    return jsonify(menus)
