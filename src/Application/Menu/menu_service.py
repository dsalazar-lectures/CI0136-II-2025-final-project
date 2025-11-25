from typing import List, Dict, Tuple, Optional
from src.Model.Menu.Menu import Menu
from src.Model.Menu.MenuDay import MenuDay
from src.Application.Recipes import recipe_service


def generate_menus(
    count: int,
) -> Tuple[Optional[Menu], Optional[List[str]], Optional[List[Dict]]]:
    """
    Generates a menu with n days, each day with breakfast, lunch, dinner and dessert.

    Returns:
        Tuple[Optional[Menu], Optional[List[str]], Optional[List[Dict]]]:
            (menu, missing_categories, menu_details)
        - If successful: (Menu, None, [list of menu details with recipes])
        - If categories are missing: (None, [list of missing categories], None)
    """
    # Dictionary of meal categories
    meal_categories = {
        "breakfast": "desayuno",
        "lunch": "almuerzo",
        "dinner": "cena",
        "dessert": "postre",
    }

    daily_menus = {}
    menu_details = []

    # Generate each day of the menu
    for day in range(1, count + 1):
        # Get a random recipe for each category
        breakfast_recipe = recipe_service.get_random_recipe_by_category(
            meal_categories["breakfast"]
        )
        lunch_recipe = recipe_service.get_random_recipe_by_category(
            meal_categories["lunch"]
        )
        dinner_recipe = recipe_service.get_random_recipe_by_category(
            meal_categories["dinner"]
        )
        dessert_recipe = recipe_service.get_random_recipe_by_category(
            meal_categories["dessert"]
        )

        # Validate that recipes were found for all categories
        missing_categories = []
        if not breakfast_recipe:
            missing_categories.append("desayuno")
        if not lunch_recipe:
            missing_categories.append("almuerzo")
        if not dinner_recipe:
            missing_categories.append("cena")
        if not dessert_recipe:
            missing_categories.append("postre")

        if missing_categories:
            return None, missing_categories, None

        # Create MenuDay with recipe IDs
        menu_day = MenuDay(
            breakfast_recipe_id=breakfast_recipe.id,
            lunch_recipe_id=lunch_recipe.id,
            dinner_recipe_id=dinner_recipe.id,
            dessert_recipe_id=dessert_recipe.id,
        )

        daily_menus[day] = menu_day

        # Add detailed menu information with full recipe data
        menu_details.append(
            {
                "day": day,
                "breakfast": breakfast_recipe.to_dict(),
                "lunch": lunch_recipe.to_dict(),
                "dinner": dinner_recipe.to_dict(),
                "dessert": dessert_recipe.to_dict(),
            }
        )

    # Create Menu object (menu_id will be assigned in the repository)
    menu = Menu(
        menu_id=0, daily_menus=daily_menus  # Will be automatically assigned when saved
    )

    return menu, None, menu_details
