from Shared.Logs.Logger_textfile import TxtFileLogger

logger = TxtFileLogger()

try:
    result1 = 10 / 2
    logger.log(
        level="info",
        user="Alice",
        role="Chef",
        action="Add recipe",
        id_object=123,
        description=f"Recipe added successfully: {result1}"
    )

    logger.log(
        level="info",
        user="Yordi",
        role="Admin",
        action="Login",
        id_object=124,
        description="User logged in successfully"
    )

    logger.log(
        level="warning",
        user="Maria",
        role="User",
        action="Select an ingredient",
        id_object=125,
        description="The ingredient is not in the list"
    )

    logger.log(
        level="info",
        user="Mario",
        role="User",
        action="Modify recipe",
        id_object=126,
        description="Recipe modified successfully"
    )

except Exception as e:
    logger.log(
        level="error",
        user="Juan",
        role="Administrator",
        action="Generate report",
        id_object=127,
        description=f"An unexpected error occurred: {str(e)}"
    )

try:
    result2 = 10 / 0
    logger.log(
        level="info",
        user="Bob",
        role="User",
        action="Login",
        id_object=128,
        description=f"Login successful: {result2}"
    )

except Exception as e:
    logger.log(
        level="error",
        user="Bob",
        role="User",
        action="Login",
        id_object=128,
        description=f"An error occurred during login: {str(e)}"
    )
