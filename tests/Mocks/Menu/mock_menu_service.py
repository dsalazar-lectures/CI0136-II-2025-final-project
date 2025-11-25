from unittest.mock import MagicMock
from src.Model.Menu.Menu import Menu
from src.Model.Menu.MenuDay import MenuDay


class MockMenuService:
    @staticmethod
    def generate_valid_menu(count):
        """Generate a valid menu with all categories"""
        menu_details = []
        daily_menus = {}

        for day in range(1, count + 1):
            menu_day = MenuDay(
                breakfast_recipe_id=1,
                lunch_recipe_id=2,
                dinner_recipe_id=3,
                dessert_recipe_id=4,
            )
            daily_menus[day] = menu_day

            menu_details.append(
                {
                    "day": day,
                    "breakfast": {"id": 1, "name": "Pancakes"},
                    "lunch": {"id": 2, "name": "Pasta"},
                    "dinner": {"id": 3, "name": "Salmón"},
                    "dessert": {"id": 4, "name": "Flan"},
                }
            )

        menu = Menu(menu_id=0, daily_menus=daily_menus)
        return menu, None, menu_details

    @staticmethod
    def generate_menu_with_missing_categories(missing):
        """Generate menu response with missing categories"""
        return None, missing, None

    @staticmethod
    def generate_empty_menu():
        """Generate empty menu for count=0"""
        menu = Menu(menu_id=0, daily_menus={})
        return menu, None, []
