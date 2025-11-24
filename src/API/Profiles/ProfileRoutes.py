from flask import Blueprint, jsonify, request
from src.Application.Profiles.ProfileUseCase import ProfileUseCase
from src.Application.Profiles.Services.ProfileApplicationService import (
    ProfileApplicationService,
)
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository

# Initialize the repository and use case
profile_repository = ProfileRepository()
profile_use_case = ProfileUseCase(profile_repository)

profiles_bp = Blueprint("profiles", __name__)
profile_service = ProfileApplicationService(ProfileRepository("profiles.csv"))


@profiles_bp.route("/profiles/<int:user_id>", methods=["GET"])
def get_profile(user_id: int):
    profile = profile_service.get_profile(user_id)
    if not profile:
        return jsonify({"error": "Perfil no encontrado"}), 404
    return jsonify(profile.to_dict()), 200


@profiles_bp.route("/profiles/<int:user_id>/favorites", methods=["PUT"])
def set_favorites(user_id: int):
    payload = request.get_json(silent=True) or {}
    ingredients = payload.get("ingredients") or []
    if not isinstance(ingredients, list):
        return (
            jsonify({"error": "Formato inválido: 'ingredients' debe ser lista."}),
            400,
        )
    updated = profile_service.set_favorite_ingredients(user_id, ingredients)
    if not updated:
        return jsonify({"error": "Perfil no encontrado"}), 404
    return jsonify(updated.to_dict()), 200


@profiles_bp.route("/profiles/<int:user_id>/favorite-menus", methods=["GET"])
def get_favorite_menus(user_id: int):
    """Get all favorite menus for a user"""
    try:
        favorite_menus = profile_use_case.get_favorite_menus(user_id)
        return jsonify({"user_id": user_id, "favorite_menus": favorite_menus}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@profiles_bp.route("/profiles/<int:user_id>/favorite-menus", methods=["POST"])
def add_favorite_menu(user_id: int):
    """Add a menu to user's favorites"""
    try:
        data = request.get_json(silent=True) or {}
        menu_id = data.get("menu_id")

        if not menu_id:
            return jsonify({"error": "menu_id is required"}), 400

        success = profile_use_case.add_favorite_menu(user_id, menu_id)

        if success:
            return (
                jsonify(
                    {
                        "message": "Menu added to favorites",
                        "user_id": user_id,
                        "menu_id": menu_id,
                    }
                ),
                201,
            )
        else:
            return (
                jsonify({"error": "Menu already in favorites or user not found"}),
                400,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@profiles_bp.route("/profiles/<int:user_id>/favorite-menus", methods=["DELETE"])
def remove_favorite_menu(user_id: int):
    """Remove a menu from user's favorites"""
    try:
        data = request.get_json(silent=True) or {}
        menu_id = data.get("menu_id")

        if not menu_id:
            return jsonify({"error": "menu_id is required"}), 400

        success = profile_use_case.remove_favorite_menu(user_id, menu_id)

        if success:
            return (
                jsonify(
                    {
                        "message": "Menu removed from favorites",
                        "user_id": user_id,
                        "menu_id": menu_id,
                    }
                ),
                200,
            )
        else:
            return (
                jsonify({"error": "Menu not found in favorites or user not found"}),
                404,
            )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@profiles_bp.route("/profiles/<int:user_id>/role", methods=["GET"])
def get_user_role(user_id: int):
    """Get role of a user"""
    try:
        profile = profile_service.get_profile(user_id)
        if not profile:
            return jsonify({"error": "Perfil no encontrado"}), 404
        role = profile.role
        return jsonify({"user_id": user_id, "role": role.name}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
