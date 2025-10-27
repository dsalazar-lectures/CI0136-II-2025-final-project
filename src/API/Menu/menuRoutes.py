from flask import Blueprint, jsonify, request
from src.Application.Recipes import recipe_service

recipes_bp = Blueprint("menu", __name__)


@recipes_bp.route("/menu", methods=["GET"])
def get_menu():
    category = request.args.get("category")
    recipes = recipe_service.get_recipes_by_category(category)
    limited_recipes = recipes[:5]
    return jsonify([recipe.to_dict() for recipe in limited_recipes])
