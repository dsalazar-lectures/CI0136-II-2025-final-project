from flask import Blueprint, jsonify, request
from src.Application.Recipes import recipe_service
from src.Application.Menu import MenuUseCase

from src.Application.Menu.CustomizedMenuService import CustomizedMenuService
from src.Application.Profiles.Services.ProfileApplicationService import ProfileApplicationService
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository

recipes_bp = Blueprint("menu", __name__)

customized_service = CustomizedMenuService()
profile_service = ProfileApplicationService(ProfileRepository("profiles.csv"))

@recipes_bp.route("/menu", methods=["GET"])
def get_menu():
    category = request.args.get("category")
    recipe = recipe_service.get_random_recipe_by_category(category)
    return jsonify([recipe.to_dict() if recipe else {}])


@recipes_bp.route("/menu/email", methods=["GET"])
def emailMenu():
    menuRecipes = request.json.get("ids")
    recipientEmail = request.json.get("sendto")
    return "", MenuUseCase.emailPdf(menuRecipes, recipientEmail)

@recipes_bp.route("/menu/customized", methods=["GET"])
def customized_menu():
    user_id = request.args.get("user_id", type=int)
    category = request.args.get("category")
    if not user_id:
        return jsonify({"error": "user_id requerido"}), 400

    profile = profile_service.get_profile(user_id)
    if not profile:
        return jsonify({"error": "Perfil no encontrado"}), 404

    recipes = customized_service.recommend_by_favorites(profile.favorite_foods, category)
    return jsonify([r.to_dict() for r in recipes]), 200
