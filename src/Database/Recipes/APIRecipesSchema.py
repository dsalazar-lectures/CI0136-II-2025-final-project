import csv
import os
import requests
from src.Model.Recipes.Recipes import Recipe

PATH = os.path.join(os.path.dirname(__file__), "APIRecipes.csv")
api_recipes = []


def get_api_data():
    """Gets recipes from API"""

    url = "https://www.themealdb.com/api/json/v1/1/search.php?s="
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("meals", [])
    except requests.exceptions.RequestException:
        return []


def parse_recipe(meal):
    """Adapts API recipe to recipe model"""
    ingredients = []
    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")
        if ingredient and ingredient.strip():
            measure_text = measure.strip() if measure and measure.strip() else ""
            if measure_text:
                ingredients.append(f"{measure_text} {ingredient.strip()}")
            else:
                ingredients.append(ingredient.strip())

    categories = []
    if meal.get("strCategory"):
        categories.append(meal["strCategory"])
    if meal.get("strArea"):
        categories.append(meal["strArea"])

    return {
        "id": meal.get("idMeal"),
        "name": meal.get("strMeal"),
        "categories": categories,
        "ingredients": ingredients,
        "duration": None,
        "instructions": meal.get("strInstructions"),
        "portions": 1,
        "author": "TheMealDB",
        "calificationsSumatory": 0,
        "calificationsAmount": 0,
        "usersUsedRecipe": 0,
        "usersRated": [],
    }


def write_api_recipes(parsed_recipes):
    """Write parsed recipes to csv"""
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
            recipe_copy = recipe.copy()
            recipe_copy["categories"] = str(recipe["categories"])
            recipe_copy["ingredients"] = str(recipe["ingredients"])
            writer.writerow(recipe_copy)


def load_api_recipes():
    """loads recipes into list"""
    global api_recipes
    api_recipes.clear()
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
                row.get("usersRated", "[]"),
            )
            api_recipes.append(recipe)


meals = get_api_data()
if meals:
    parsed_recipes = [parse_recipe(meal) for meal in meals]
    write_api_recipes(parsed_recipes)
