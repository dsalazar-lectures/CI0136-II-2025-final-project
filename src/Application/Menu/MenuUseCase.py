import re
from src.Application.Menu.MenuPdfAdapter import MenuPdfAdapter
from src.Services.EmailService import sendMenu


def emailPdf(recipeList, recipientEmail):

    if not re.match("[^@]+@[^@]+\.[^@]+", recipientEmail):
        return 400

    adapter = MenuPdfAdapter(recipeList)
    sendMenu(recipientEmail, adapter)

    return 200
