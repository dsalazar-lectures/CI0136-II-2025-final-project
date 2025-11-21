import csv
import os


class MenuCSV:
    def __init__(self, file_path):
        self.file_path = file_path
        self.headers = [
            "menu_id",
            "day",
            "breakfast_recipe_id",
            "lunch_recipe_id",
            "dinner_recipe_id",
            "dessert_recipe_id",
        ]
        # Ensure the CSV file exists and has headers
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                # Format: menu_id, day, breakfast, lunch, dinner, dessert
                writer.writerow(self.headers)

    def menu_exists(self, menu_id: int) -> bool:
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["menu_id"] == str(menu_id):
                    return True
        return False

    def create_menu(self, menu_data):
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

        new_menu = {
            "menu_id": str(next_id),
            "daily_menus": menu_data.daily_menus,
        }

        # Write each day as a separate row
        with open(self.file_path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            for day, menu_day in new_menu["daily_menus"].items():
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
        return new_menu

    def get_menu_by_id(self, menu_id: int):
        daily_menus = {}
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for csv_row in reader:
                if csv_row["menu_id"] == str(menu_id):
                    day = int(csv_row["day"])
                    daily_menus[day] = {
                        "breakfast_recipe_id": int(csv_row["breakfast_recipe_id"]),
                        "lunch_recipe_id": int(csv_row["lunch_recipe_id"]),
                        "dinner_recipe_id": int(csv_row["dinner_recipe_id"]),
                        "dessert_recipe_id": int(csv_row["dessert_recipe_id"]),
                    }

        if daily_menus:
            return {"menu_id": menu_id, "daily_menus": daily_menus}
        return None

    def delete_menu(self, menu_id: int) -> bool:
        # Store all rows except those with the specified menu_id
        rows = []
        menu_found = False

        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["menu_id"] == str(menu_id):
                    menu_found = True
                    # Skip rows with the specified menu_id
                    continue
                rows.append(row)

        if menu_found:
            # Write back the remaining rows to the CSV file
            with open(self.file_path, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(rows)

        return menu_found

    def list_menus(self) -> list:
        menus = {}
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for csv_row in reader:
                menu_id = int(csv_row["menu_id"])
                day = int(csv_row["day"])
                if menu_id not in menus:
                    menus[menu_id] = {}
                menus[menu_id][day] = {
                    "breakfast_recipe_id": int(csv_row["breakfast_recipe_id"]),
                    "lunch_recipe_id": int(csv_row["lunch_recipe_id"]),
                    "dinner_recipe_id": int(csv_row["dinner_recipe_id"]),
                    "dessert_recipe_id": int(csv_row["dessert_recipe_id"]),
                }

        # Convert to list of menu dictionaries
        menu_list = []
        for menu_id, daily_menus in menus.items():
            menu_list.append({"menu_id": menu_id, "daily_menus": daily_menus})

        return menu_list
