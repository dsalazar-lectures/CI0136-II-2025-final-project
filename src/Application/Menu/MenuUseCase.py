import re
import time
from src.Application.Recipes import recipe_service
from src.Infrastructure.Menu.MenuRepository import MenuRepository
from src.Model.Menu.MenuDay import MenuDay
from src.Model.Menu.Menu import Menu
from src.Application.Menu.MenuPdfAdapter import MenuPdfAdapter
from src.Services.EmailService import sendMenu

menu_repository = MenuRepository()


def generateRandomMenu():
    meal_categories = {
        "breakfast": ["desayuno", "breakfast"],
        "lunch": ["almuerzo", "lunch"],
        "dinner": ["cena", "dinner"],
        "dessert": ["postre", "dessert"],
    }

    recipe = recipe_service.get_random_recipe_by_categories(
        meal_categories["breakfast"]
    )
    breakfast_recipe_id = recipe.id if recipe else 0
    recipe = recipe_service.get_random_recipe_by_categories(meal_categories["lunch"])
    lunch_recipe_id = recipe.id if recipe else 0
    recipe = recipe_service.get_random_recipe_by_categories(meal_categories["dinner"])
    dinner_recipe_id = recipe.id if recipe else 0
    recipe = recipe_service.get_random_recipe_by_categories(meal_categories["dessert"])
    dessert_recipe_id = recipe.id if recipe else 0

    menu_day = MenuDay(
        breakfast_recipe_id, lunch_recipe_id, dinner_recipe_id, dessert_recipe_id
    )

    daily_menu = dict()
    daily_menu[1] = menu_day

    menu = Menu(0, daily_menu)

    menu, message, code = menu_repository.create_menu(menu)

    return menu


def emailPdf(recipeList, recipientEmail):

    if not re.match("[^@]+@[^@]+\.[^@]+", recipientEmail):
        return 400

    adapter = MenuPdfAdapter(recipeList)
    retryDelay = 3

    for x in range(3):
        error = sendMenu(recipientEmail, adapter)
        if (
            error != 450 or error != 454
        ):  # mailbox busy or temporarily blocked or temporary authentication problem
            break
        time.sleep(retryDelay)

    return 204
