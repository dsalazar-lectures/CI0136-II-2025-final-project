from itertools import chain
import os
from Application.Interfaces.IMenuAdapter import IMenuAdapter
from src.Application.Recipes import recipe_service
from fpdf import FPDF

class MenuPdfAdapter(IMenuAdapter):
    def __init__(self, recipesId):
        self.recipeList = recipesId
        self.fileType = "pdf"

    def generateContentFile(self):
        
        
        pdfMenu = FPDF(orientation='P', unit='mm', format='A4')
        pdfMenu.set_margins(left=25, top=30, right=25)
        pdfMenu.set_auto_page_break(True, margin=10)
        pdfMenu.add_page()

        pdfMenu.set_font(family='Times', size=30)
        pdfMenu.set_text_color(r = 0, g = 0, b = 0)

        recipe = "Menu solicitado"

        pdfMenu.cell(w=pdfMenu.w, txt=recipe, align="J")
        pdfMenu.set_font(family='Times', size=15)
        pdfMenu.multi_cell(w=pdfMenu.w - 50, h=20, txt=' ', align="J")

        for id in self.recipeList:
           recipe = recipe_service.get_recipe_by_id(int(id))
           print(recipe.name)
           pdfMenu.multi_cell(w=pdfMenu.w - 50, h=20, txt=recipe.name, align="J")
           pdfMenu.multi_cell(w=pdfMenu.w  - 50, h=20, txt="Ingredientes:" + (" ".join(str(i) for i in chain(recipe.ingredients))), align="J")
           pdfMenu.multi_cell(w=pdfMenu.w  - 50, h=20, txt= "Instrucciones: " + recipe.instructions, align="J")
           pdfMenu.multi_cell(w=pdfMenu.w - 50, h=10, txt=' ', align="J")

        pdfMenu.output("menu.pdf")
        content = open('menu.pdf', 'rb').read()
        os.remove("menu.pdf")
        return content

    def getFileExtension(self):
        return self.fileType