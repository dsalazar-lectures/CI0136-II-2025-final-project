import csv
import os
from src.Model.Recipes.Recipes import Recipe

PATH = os.path.join(os.path.dirname(__file__), "RecipesExamples.csv")

system_recipes = []


def load_recipes():
    global system_recipes
    with open(PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        system_recipes = [
            Recipe(
                row["id"],
                row["name"],
                row["categories"],
                row["ingredients"],
                row["duration"],
                row["instructions"],
                row["portions"],
                row["author"],
                row["calificationsSumatory"],
                row["calificationsAmount"],
                row["usersUsedRecipe"],
            )
            for row in reader
        ]


load_recipes()
