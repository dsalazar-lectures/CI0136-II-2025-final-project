import os
from Application.Interfaces.IMenuAdapter import IMenuAdapter
from src.Application.Recipes import recipe_service

class MenuPdfAdapter(IMenuAdapter):
    def __init__(self, recipesId):
        self.recipeList = recipesId
        self.fileType = "pdf"

    def generateContentFile(self):
        
        for id in self.recipeList:
           print(id)
           print(recipe_service.get_recipe_by_id(int(id)))
        
        f = open("example.txt", "w")
        f.close()
        content = open('example.txt', 'rb').read()
        os.remove("example.txt")
        return content

    def getFileExtension(self):
        return self.fileType