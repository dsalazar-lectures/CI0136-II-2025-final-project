from flask import request
from src.Application.Recipes import recipe_service
from src.Infrastructure.User.UserRepository import UserRepository

user_repository = UserRepository()


def get_username_from_request():
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return None
    
    parts = auth_header.split()
    
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    
    token = parts[1]
    user_dto = user_repository.get_user_by_token(token)
    return user_dto.username if user_dto else None


def create_recipe_controller(data):
    username = get_username_from_request()
    
    if not username:
        return 401, {
            "error": "Proporcione un token valido en Authorization: Bearer <token>"
        }
    
    recipe = recipe_service.create_recipe(data, username)
    
    if recipe == -1:
        return 400, {
            "error": "Se necesita información adicional sobre la receta"
        }
    
    return 201, {
        "message": "Receta creada exitosamente",
        "recipe": recipe.to_dict()
    }


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
        return 403, {
            "error": "No autorizado para eliminar esta receta"
        }
    
    return 200, {
        "message": "Receta eliminada",
        "recipe": result.__str__()
    }


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