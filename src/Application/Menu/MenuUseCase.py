import re
import time
from src.Application.Menu.MenuPdfAdapter import MenuPdfAdapter
from src.Services.EmailService import sendMenu
from src.Shared.Logs.custom_logger import CustomLogger

logger = CustomLogger()


def emailPdf(recipeList, recipientEmail):

    if not re.match("[^@]+@[^@]+\\.[^@]+", recipientEmail):
        logger.log(
            level="error",
            user="system",
            role="-",
            action="Email menu PDF",
            id_object="-",
            description=f"Invalid email format: {recipientEmail}",
        )
        return 400

    adapter = MenuPdfAdapter(recipeList)
    retryDelay = 3

    for x in range(3):
        error = sendMenu(recipientEmail, adapter)
        if (
            error != 450 or error != 454
        ):  # mailbox busy or temporarily blocked or temporary authentication problem
            if error in [450, 454]:
                logger.log(
                    level="warning",
                    user="system",
                    role="-",
                    action="Email menu PDF",
                    id_object="-",
                    description=f"Retry attempt {x + 1} for email {recipientEmail}, error code: {error}",
                )
            break
        time.sleep(retryDelay)

    if error == 204 or error not in [450, 454]:
        logger.log(
            level="info",
            user="system",
            role="-",
            action="Email menu PDF",
            id_object="-",
            description=f"Menu PDF sent successfully to {recipientEmail}",
        )
    else:
        logger.log(
            level="error",
            user="system",
            role="-",
            action="Email menu PDF",
            id_object="-",
            description=f"Failed to send menu PDF to {recipientEmail} after retries, error code: {error}",
        )

    return 204
