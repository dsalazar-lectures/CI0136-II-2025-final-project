from flask import request
from src.Application.Recipes import recipe_service
from src.Infrastructure.User.UserRepository import UserRepository

user_repository = UserRepository()


def get_username_from_request():
    user_id = request.args.get("user_id", type=int)

    if not user_id:
        return None
    
    user = user_repository.get_user_by_id(user_id)
    if not user:
        return None

    return user.username


def create_recipe_controller(data):
    username = get_username_from_request()

    if not username:
        return 401, {
            "error": "Proporcione un token valido en Authorization: Bearer <token>"
        }

    recipe = recipe_service.create_recipe(data, username)

    if recipe == -1:
        return 400, {"error": "Se necesita información adicional sobre la receta"}

    return 201, {"message": "Receta creada exitosamente", "recipe": recipe.to_dict()}


def delete_recipe_controller(recipe_id):
    username = get_username_from_request()

    if not username:
        return 401, {
            "error": "Proporcione un token valido en Authorization: Bearer <token>"
        }

    result = recipe_service.delete_recipe(recipe_id, username)

    if result is None:
        return 404, {"error": "Receta no encontrada"}

    if result is False:
        return 403, {"error": "No autorizado para eliminar esta receta"}

    return 200, {"message": "Receta eliminada", "recipe": result.__str__()}


def update_recipe_controller(recipe_id, updates):
    username = get_username_from_request()

    if not username:
        return 401, {
            "error": "Proporcione un token valido en Authorization: Bearer <token>"
        }

    allowed_fields = {
        "name",
        "categories",
        "ingredients",
        "duration",
        "instructions",
        "portions",
    }
    safe_updates = {k: v for k, v in updates.items() if k in allowed_fields}

    result = recipe_service.update_recipe(recipe_id, safe_updates, username)

    if result == -1:
        return 400, {"error": "Datos de actualización inválidos"}
    if result is None:
        return 404, {"error": "Receta no encontrada"}
    if result is False:
        return 403, {"error": "No autorizado para editar esta receta"}

    return 200, result.to_dict()

def rate_recipe_controller(recipe_id, data):
    username = get_username_from_request()

    if not username:
        return 401, {"error": "Debe enviar un token válido"}

    if "rating" not in data:
        return 400, {"error": "Se requiere 'rating' (1 a 5)"}

    result = recipe_service.rate_recipe(recipe_id, username, data["rating"])

    if result is None:
        return 404, {"error": "Receta no encontrada"}

    if result is False:
        return 403, {"error": "Ya calificó esta receta"}

    if result == -1:
        return 400, {"error": "Rating inválido (debe ser 1 a 5)"}

    return 200, {"message": "Calificación registrada", "recipe": result.to_dict()}

