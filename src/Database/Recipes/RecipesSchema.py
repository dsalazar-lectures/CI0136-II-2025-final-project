import csv
import os
from src.Model.Recipes.Recipes import Recipe

PATH = os.path.join(os.path.dirname(__file__), "RecipesExamples.csv")

system_recipes = []


def load_recipes():
    global system_recipes
    system_recipes.clear()

    with open(PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipe = Recipe(
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
                row["usersRated"],
            )
            system_recipes.append(recipe)


load_recipes()
