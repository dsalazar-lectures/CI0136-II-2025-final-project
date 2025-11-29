import csv
import os
from src.Model.Recipes.Recipes import Recipe
from src.Database.Recipes.TheMealDBAdapter import TheMealDBAdapter

PATH = os.path.join(os.path.dirname(__file__), "APIRecipes.csv")
api_recipes = []


def load_api_recipes():
    """loads recipes into list"""
    global api_recipes
    api_recipes.clear()

    adapter = TheMealDBAdapter()
    meals = adapter.get_raw_data()

    if meals:
        parsed_recipes = [adapter.parse_recipe(meal) for meal in meals]

        write_api_recipes(parsed_recipes)

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
            )
            api_recipes.append(recipe)


def write_api_recipes(parsed_recipes):
    """Writes parsed recipes to csv"""
    with open(PATH, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "id",
            "name",
            "categories",
            "ingredients",
            "duration",
            "instructions",
            "portions",
            "author",
            "calificationsSumatory",
            "calificationsAmount",
            "usersUsedRecipe",
            "usersRated",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for recipe in parsed_recipes:
            row_dict = {
                "id": recipe["id"],
                "name": recipe["name"],
                "categories": recipe["categories"],
                "ingredients": recipe["ingredients"],
                "duration": recipe["duration"] if recipe["duration"] else "",
                "instructions": recipe["instructions"],
                "portions": recipe["portions"],
                "author": recipe["author"],
                "calificationsSumatory": recipe["calificationsSumatory"],
                "calificationsAmount": recipe["calificationsAmount"],
                "usersUsedRecipe": recipe["usersUsedRecipe"],
            }
            writer.writerow(row_dict)


load_api_recipes()
