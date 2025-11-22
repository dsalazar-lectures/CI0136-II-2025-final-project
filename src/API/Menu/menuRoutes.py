from flask import Blueprint, jsonify, request
from src.Application.Recipes import recipe_service
from src.Application.Menu import menu_service
from src.Application.Menu import MenuUseCase

import threading

_slot_counters = {"breakfast": 0, "lunch": 0, "dinner": 0, "dessert": 0}
_slot_lock = threading.Lock()

from src.Application.Menu.CustomizedMenuService import CustomizedMenuService
from src.Application.Profiles.Services.ProfileApplicationService import (
    ProfileApplicationService,
)
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository

# Factory function to create blueprints with configurable profiles.csv path
def create_menu_blueprints(profiles_csv_path="profiles.csv"):
    menu_bp = Blueprint("menu", __name__)
    recipes_bp = Blueprint("menu_recipes", __name__)

    customized_service = CustomizedMenuService()
    profile_service = ProfileApplicationService(ProfileRepository(profiles_csv_path))

    @menu_bp.route("/menu", methods=["GET"])
    def get_menu():

        from collections import OrderedDict

        slot_category_preferences = {
            "breakfast": ["desayuno", "breakfast"],
            "lunch": ["almuerzo", "lunch"],
            "dinner": ["cena", "dinner"],
            "dessert": ["postre", "dessert"],
        }

        ordered = OrderedDict()

        for slot, prefs in slot_category_preferences.items():
            found = None
            chosen_recipe = None
            chosen_list_len = 0
            for cat in prefs:
                recipes = recipe_service.get_recipes_by_category(cat)
                if recipes:
                    chosen_list_len = len(recipes)
                    with _slot_lock:
                        idx = _slot_counters.get(slot, 0) % chosen_list_len
                        _slot_counters[slot] = _slot_counters.get(slot, 0) + 1
                    chosen_recipe = recipes[idx]
                    break

            if chosen_recipe:
                ordered[slot] = chosen_recipe.to_dict()
            else:
                ordered[slot] = {}

        return jsonify(ordered)

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

    @recipes_bp.route("/menu/customized", methods=["GET"])
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

    return menu_bp, recipes_bp
