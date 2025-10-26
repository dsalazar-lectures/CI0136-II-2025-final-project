from src.Application.Menu.MenuPdfAdapter import MenuPdfAdapter
from src.Services.EmailService import sendMenu


def emailPdf(recipeList, recipientEmail):

    adapter = MenuPdfAdapter(recipeList)
    sendMenu(recipientEmail, adapter)

    return "200"
