from flask import Blueprint, jsonify, request
from src.Application.Recipes import recipe_service
from src.Application.Menu import MenuUseCase

recipes_bp = Blueprint("menu", __name__)


@recipes_bp.route("/menu", methods=["GET"])
def get_menu():
    category = request.args.get("category")
    recipe = recipe_service.get_random_recipe_by_category(category)
    return jsonify([recipe.to_dict() if recipe else {}])


@recipes_bp.route("/menu/email", methods=["GET"])
def emailMenu():
    menuRecipes = request.json.get("ids")
    recipientEmail = request.json.get("sendto")
    return jsonify(MenuUseCase.emailPdf(menuRecipes, recipientEmail))
