import re
import time
from src.Application.Menu.MenuPdfAdapter import MenuPdfAdapter
from src.Services.EmailService import sendMenu


def emailPdf(recipeList, recipientEmail):

    if not re.match("[^@]+@[^@]+\.[^@]+", recipientEmail):
        return 400

    adapter = MenuPdfAdapter(recipeList)
    retryDelay = 3

    for x in range(3):
        error = sendMenu(recipientEmail, adapter)
        if (
            error == 450 or error == 454
        ):  # mailbox busy or temporarily blocked or temporary authentication problem
            break
        time.sleep(retryDelay)

    return 200
