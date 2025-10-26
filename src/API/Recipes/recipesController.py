from src.Application.Recipes import recipe_service

def update_recipe_controller(recipe_id, updates, username):

    allowed_fields = {"name", "categories", "ingredients", "duration", "instructions", "portions"}
    safe_updates = {k: v for k, v in updates.items() if k in allowed_fields}

    result = recipe_service.update_recipe(recipe_id, safe_updates, username)

    if result == -1:
        return 400, {"error": "Datos de actualización inválidos"}
    if result is None:
        return 404, {"error": "Receta no encontrada"}
    if result is False:
        return 403, {"error": "No autorizado para editar esta receta"}

    return 200, result.to_dict()
