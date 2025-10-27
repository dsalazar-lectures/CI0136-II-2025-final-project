from flask import Blueprint, jsonify, request
from src.Application.Profiles.ProfileUseCase import ProfileUseCase
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository

# Initialize the repository and use case
profile_repository = ProfileRepository()
profile_use_case = ProfileUseCase(profile_repository)

profiles_bp = Blueprint("profiles", __name__)


@profiles_bp.route("/profiles/<string:user_id>/favorite-menus", methods=["GET"])
def get_favorite_menus(user_id: str):
    """Get all favorite menus for a user"""
    try:
        favorite_menus = profile_use_case.get_favorite_menus(user_id)
        return jsonify({
            "user_id": user_id,
            "favorite_menus": favorite_menus
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@profiles_bp.route("/profiles/<string:user_id>/favorite-menus", methods=["POST"])
def add_favorite_menu(user_id: str):
    """Add a menu to user's favorites"""
    try:
        data = request.get_json()
        menu_id = data.get("menu_id")

        if not menu_id:
            return jsonify({"error": "menu_id is required"}), 400

        success = profile_use_case.add_favorite_menu(user_id, menu_id)

        if success:
            return jsonify({
                "message": "Menu added to favorites",
                "user_id": user_id,
                "menu_id": menu_id
            }), 201
        else:
            return jsonify({
                "error": "Menu already in favorites or user not found"
            }), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@profiles_bp.route("/profiles/<string:user_id>/favorite-menus/<string:menu_id>", methods=["DELETE"])
def remove_favorite_menu(user_id: str, menu_id: str):
    """Remove a menu from user's favorites"""
    try:
        success = profile_use_case.remove_favorite_menu(user_id, menu_id)

        if success:
            return jsonify({
                "message": "Menu removed from favorites",
                "user_id": user_id,
                "menu_id": menu_id
            }), 200
        else:
            return jsonify({
                "error": "Menu not found in favorites or user not found"
            }), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
