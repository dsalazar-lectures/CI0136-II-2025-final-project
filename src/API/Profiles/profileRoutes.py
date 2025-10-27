from flask import Blueprint, jsonify, request
from src.Application.Profiles.Services.ProfileApplicationService import ProfileApplicationService
from src.Infrastructure.Profiles.ProfileRepository import ProfileRepository

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
        return jsonify({"error": "Formato inválido: 'ingredients' debe ser lista."}), 400
    updated = profile_service.set_favorite_ingredients(user_id, ingredients)
    if not updated:
        return jsonify({"error": "Perfil no encontrado"}), 404
    return jsonify(updated.to_dict()), 200
