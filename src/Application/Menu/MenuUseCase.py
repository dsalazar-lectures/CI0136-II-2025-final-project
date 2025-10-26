from src.Application.Menu.MenuPdfAdapter import MenuPdfAdapter
from src.Services.EmailService import send_file


def emailPdf(recipeList, recipientEmail):

    adapter = MenuPdfAdapter(recipeList)
    send_file(recipientEmail, adapter)

    return "200"
