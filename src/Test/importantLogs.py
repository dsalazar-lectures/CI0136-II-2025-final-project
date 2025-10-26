from src.Shared.Logs.Logger_jsonfile import JsonFileLogger

logger = JsonFileLogger()

# CREATE
try:
    recipe_id = 123
    logger.importantLog(
        level="info",
        user="Alice",
        role="Chef",
        action="Create recipe",
        id_object=recipe_id,
        description=f"Recipe created with id={recipe_id}",
    )
except Exception as e:
    logger.importantLog(
        level="error",
        user="Alice",
        role="Chef",
        action="Create recipe",
        id_object=recipe_id,
        description=f"Error creating recipe: {e}",
    )

# READ
try:
    recipe_id = 124
    recipe = {"id": recipe_id, "name": "Pasta Alfredo"}
    logger.importantLog(
        level="info",
        user="Mario",
        role="User",
        action="Get recipe",
        id_object=recipe_id,
        description=f"Recipe fetched: {recipe}",
    )
except KeyError:
    logger.importantLog(
        level="warning",
        user="Mario",
        role="User",
        action="Get recipe",
        id_object=recipe_id,
        description=f"Recipe not found: id={recipe_id}",
    )
except Exception as e:
    logger.importantLog(
        level="error",
        user="Mario",
        role="User",
        action="Get recipe",
        id_object=recipe_id,
        description=f"Unexpected error: {e}",
    )

# UPDATE
try:
    recipe_id = 125
    updated = True
    if updated:
        logger.importantLog(
            level="info",
            user="Mario",
            role="User",
            action="Update recipe",
            id_object=recipe_id,
            description=f"Recipe {recipe_id} updated successfully",
        )
    else:
        logger.importantLog(
            level="warning",
            user="Mario",
            role="User",
            action="Update recipe",
            id_object=recipe_id,
            description=f"No changes applied to recipe {recipe_id}",
        )
except Exception as e:
    logger.importantLog(
        level="error",
        user="Mario",
        role="User",
        action="Update recipe",
        id_object=recipe_id,
        description=f"Update failed for {recipe_id}: {e}",
    )

# DELETE
try:
    recipe_id = 999
    deleted = False
    if not deleted:
        raise ValueError("Recipe is referenced by orders")
    logger.importantLog(
        level="info",
        user="Yordi",
        role="Admin",
        action="Delete recipe",
        id_object=recipe_id,
        description=f"Recipe {recipe_id} deleted",
    )
except ValueError as e:
    logger.importantLog(
        level="warning",
        user="Yordi",
        role="Admin",
        action="Delete recipe",
        id_object=recipe_id,
        description=f"Cannot delete recipe {recipe_id}: {e}",
    )
except Exception as e:
    logger.importantLog(
        level="error",
        user="Yordi",
        role="Admin",
        action="Delete recipe",
        id_object=recipe_id,
        description=f"Unexpected delete error {recipe_id}: {e}",
    )


# Login correcto
try:
    user = "carla"
    logger.importantLog(
        level="info",
        user=user,
        role="User",
        action="Login",
        id_object=126,
        description="User authenticated successfully",
    )
except Exception as e:
    logger.importantLog(
        level="error",
        user="carla",
        role="User",
        action="Login",
        id_object=126,
        description=f"Login error: {e}",
    )

# Login fallido
try:
    user = "diego"
    raise PermissionError("Invalid credentials")
except PermissionError as e:
    logger.importantLog(
        level="warning",
        user=user,
        role="User",
        action="Login",
        id_object=127,
        description=f"Login failed: {e}",
    )
except Exception as e:
    logger.importantLog(
        level="error",
        user=user,
        role="User",
        action="Login",
        id_object=127,
        description=f"Unexpected login error: {e}",
    )

# Cuenta bloqueada tras varios intentos
try:
    user = "laura"
    attempts = 5
    if attempts >= 5:
        raise PermissionError("Account locked for 15 minutes")
except PermissionError as e:
    logger.importantLog(
        level="warning",
        user=user,
        role="User",
        action="Account lock",
        id_object=128,
        description=str(e),
    )
