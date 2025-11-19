import csv
import os
from src.Model.Menu.Menu import Menu
from src.Model.Menu.MenuDay import MenuDay


class MenuCSV:
    def __init__(self, file_path):
        self.file_path = file_path
        # Ensure the CSV file exists and has headers
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                # Format: menu_id, day, breakfast, lunch, dinner, dessert
                writer.writerow(
                    [
                        "menu_id",
                        "day",
                        "breakfast_recipe_id",
                        "lunch_recipe_id",
                        "dinner_recipe_id",
                        "dessert_recipe_id",
                    ]
                )

    def menu_exists(self, menu_id: int) -> bool:
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["menu_id"] == str(menu_id):
                    return True
        return False

    def create_menu(self, menu: Menu):
        next_id = 1
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", newline="") as file:
                reader = csv.DictReader(file)
                # Collect existing IDs
                ids = [
                    int(row["menu_id"]) for row in reader if row["menu_id"].isdigit()
                ]
                if ids:
                    next_id = max(ids) + 1

        # Write each day as a separate row
        with open(self.file_path, "a", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "menu_id",
                    "day",
                    "breakfast_recipe_id",
                    "lunch_recipe_id",
                    "dinner_recipe_id",
                    "dessert_recipe_id",
                ],
            )
            for day, menu_day in menu.daily_menus.items():
                writer.writerow(
                    {
                        "menu_id": str(next_id),
                        "day": str(day),
                        "breakfast_recipe_id": str(menu_day.breakfast),
                        "lunch_recipe_id": str(menu_day.lunch),
                        "dinner_recipe_id": str(menu_day.dinner),
                        "dessert_recipe_id": str(menu_day.dessert),
                    }
                )

        # Return the Menu object
        return Menu(menu_id=next_id, daily_menus=menu.daily_menus)

    def get_menu_by_id(self, menu_id: int) -> Menu:
        if not os.path.exists(self.file_path):
            return None

        daily_menus = {}
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for csv_row in reader:
                if csv_row["menu_id"] == str(menu_id):
                    day = int(csv_row["day"])
                    daily_menus[day] = MenuDay(
                        breakfast_recipe_id=int(csv_row["breakfast_recipe_id"]),
                        lunch_recipe_id=int(csv_row["lunch_recipe_id"]),
                        dinner_recipe_id=int(csv_row["dinner_recipe_id"]),
                        dessert_recipe_id=int(csv_row["dessert_recipe_id"]),
                    )

        if daily_menus:
            return Menu(menu_id=menu_id, daily_menus=daily_menus)
        return None
