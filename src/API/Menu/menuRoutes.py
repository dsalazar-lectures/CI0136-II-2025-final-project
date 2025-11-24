from flask import Blueprint, jsonify, request
from src.Application.Recipes import recipe_service
from src.Application.Menu import menu_service
from src.Application.Menu import MenuUseCase

from src.Application.Menu.CustomizedMenuService import CustomizedMenuService
from src.Application.Profiles.Services.ProfileApplicationService import (
    ProfileApplicationService,
)

from src.Infrastructure.Menu.MenuRepository import MenuRepository
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository

menu_bp = Blueprint("menu", __name__)
recipes_bp = Blueprint("menu", __name__)

customized_service = CustomizedMenuService()
profile_service = ProfileApplicationService(ProfileRepository("profiles.csv"))


@menu_bp.route("/menu", methods=["GET"])
def get_menu():
    category = request.args.get("category")
    recipe = recipe_service.get_random_recipe_by_category(category)
    return jsonify([recipe.to_dict() if recipe else {}])


@menu_bp.route("/menu/<string:category>/<int:count>", methods=["GET"])
def get_menus_number(category: str, count: int):
    """Generate N menus for a given category using path parameters.
    Example: GET /api/menu/almuerzo/5
    """
    # Validate count
    if count < 1:
        return (
            jsonify(
                {
                    "error": "el número de menús a generar debe ser un número entero positivo"
                }
            ),
            400,
        )
    # Category comes from the path; simply fetch recipes
    recipes = recipe_service.get_recipes_by_category(category)
    if not recipes:
        return (
            jsonify(
                {"message": f"No se encontraron recetas en la categoría '{category}'"}
            ),
            404,
        )
    # Generate menus
    menus = menu_service.generate_menus(recipes, count)
    return jsonify(menus)


@menu_bp.route("/menu/email", methods=["GET"])
def emailMenu():
    menuRecipes = request.json.get("ids")
    recipientEmail = request.json.get("sendto")
    return "", MenuUseCase.emailPdf(menuRecipes, recipientEmail)


@menu_bp.route("/menu/customized", methods=["GET", "POST"])
def customized_menu():
    user_id = request.args.get("user_id", type=int)
    category = request.args.get("category")

    if not user_id:
        return jsonify({"error": "user_id requerido"}), 400

    profile = profile_service.get_profile(user_id)
    if not profile:
        return jsonify({"error": "Perfil no encontrado"}), 404

    recipes = customized_service.recommend_by_favorites(
        profile.favorite_foods, category
    )
    recipes_data = [r.to_dict() for r in recipes]

    # View recipes
    if request.method == "GET":
        return (
            jsonify(
                {
                    "recipes": recipes_data,
                }
            ),
            200,
        )

    # Save recipe menus
    menu_repo = MenuRepository()
    menu_obj, msg, status = menu_repo.create_customized_menu(recipes)

    menu_id = menu_obj.menu_id if menu_obj else None

    return (
        jsonify({"recipes": recipes_data, "menu_id": menu_id, "message": msg}),
        status,
    )
