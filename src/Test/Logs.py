from src.Shared.Logger_component import CustomLogger

logger = CustomLogger()

try:
    result1 = 10 / 2 
    logger.log(
        level="info",
        usuario="Alice",
        rol="Chef",
        accion="Add recipe",
        descripcion=f"Recipe added successfully: {result1}"
    )

    logger.log(
        level="info",
        usuario="Yordi",
        rol="Admin",
        accion="Login",
        descripcion="User logged in successfully"
    )

    logger.log(
        level="warning",
        usuario="Maria",
        rol="User",
        accion="Select an ingredient",
        descripcion="The ingredient is not in the list"
    )

    logger.log(
        level="info",  
        usuario="Mario",
        rol="User",
        accion="Modify recipe",
        descripcion="Recipe modified successfully"
    )

except Exception as e:
    logger.log(
        level="error",
        usuario="Juan",
        rol="Administrator",
        accion="Generate report",
        descripcion=f"An unexpected error occurred: {str(e)}"
    )

try:
    result2 = 10 / 0  
    logger.log(
        level="info",
        usuario="Bob",
        rol="User",
        accion="Login",
        descripcion=f"Login successful: {result2}"
    )

except Exception as e:
    logger.log(
        level="error",
        usuario="Bob",
        rol="User",
        accion="Login",
        descripcion=f"An error occurred during login: {str(e)}"
    )
