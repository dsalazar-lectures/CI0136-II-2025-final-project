from flask import Blueprint, jsonify, request
from src.Application.Menu import menu_service
from src.Application.Menu import MenuUseCase

from src.Application.Menu.CustomizedMenuService import CustomizedMenuService
from src.Application.Profiles.Services.ProfileApplicationService import (
    ProfileApplicationService,
)

from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository
from src.Infrastructure.Menu.MenuRepository import MenuRepository

menu_bp = Blueprint("menu", __name__)

customized_service = CustomizedMenuService()
profile_service = ProfileApplicationService(ProfileRepository("profiles.csv"))
# instantiate repository lazily to avoid import-time side-effects in tests
menu_repository = MenuRepository()


@menu_bp.route("/menu", methods=["GET"])
def get_menu():
    menu = MenuUseCase.generateRandomMenu()

    return jsonify(menu.to_dict())


@menu_bp.route("/menu/<int:count>", methods=["GET"])
def get_menus_number(count: int):
    """Generate N days of menus with breakfast, lunch, dinner and dessert.
    Example: GET /api/menu/7  (generates 7 days of complete menus)
    """
    # Validate count
    if count < 1:
        return (
            jsonify({"error": "el número de días debe ser un número entero positivo"}),
            400,
        )

    # Generate menus
    menu, missing_categories, menu_details = menu_service.generate_menus(count)

    if missing_categories:
        return (
            jsonify(
                {
                    "error": f"No hay recetas disponibles para las siguientes categorías: {', '.join(missing_categories)}"
                }
            ),
            404,
        )

    # Save menu to repository (instantiate repo if not available)
    repo = menu_repository or MenuRepository()
    saved_menu, message, status_code = repo.create_menu(menu)

    if status_code != 201:
        return jsonify({"error": message}), status_code

    return jsonify({"menu_id": saved_menu.menu_id, "daily_menus": menu_details}), 201


@menu_bp.route("/menu/email", methods=["GET"])
def emailMenu():
    menuRecipes = request.json.get("ids")
    recipientEmail = request.json.get("sendto")
    return "", MenuUseCase.emailPdf(menuRecipes, recipientEmail)


@menu_bp.route("/menu/customized", methods=["GET"])
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
    return jsonify([r.to_dict() for r in recipes]), 200
