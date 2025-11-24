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

    def save_customized(self, recipes: list, day: int = 1) -> int:
        """
        Save a customized menu based on user preferences.
        """
        # Determine next menu_id based on existing rows in the CSV
        next_menu_id = 1
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", newline="") as file:
                reader = csv.DictReader(file)
                existing_ids = [
                    int(row["menu_id"]) for row in reader if row["menu_id"].isdigit()
                ]
                if existing_ids:
                    next_menu_id = max(existing_ids) + 1

        # Mapping of meal types to category keywords
        meal_category_map = {
            "breakfast": ["desayuno", "desayunos", "breakfast"],
            "lunch": ["almuerzo", "almuerzos", "comida", "lunch"],
            "dinner": ["cena", "cenas", "dinner"],
            "dessert": ["postre", "postres", "dessert"],
        }

        def detect_meal_for_recipe(recipe):
            """
            Try to determine the meal type (breakfast/lunch/dinner/dessert)
            for a given recipe based on its categories.
            """
            categories_lower = []
            try:
                categories_lower = [c.lower() for c in recipe.categories]
            except Exception:
                # If the recipe has no categories attribute or it's malformed,
                # we simply leave the list empty and fall back later.
                pass

            for meal_type, keywords in meal_category_map.items():
                for keyword in keywords:
                    if any(keyword in category for category in categories_lower):
                        return meal_type
            return None

        # Collect recipe IDs per meal type
        meal_recipe_ids = {
            "breakfast": [],
            "lunch": [],
            "dinner": [],
            "dessert": [],
        }

        # First pass: assign recipes based on detected meal from categories
        for recipe in recipes:
            meal_type = detect_meal_for_recipe(recipe)
            if meal_type:
                meal_recipe_ids[meal_type].append(str(recipe.id))

        # Second pass: unassigned recipes are distributed by position
        unassigned_recipes = [r for r in recipes if detect_meal_for_recipe(r) is None]
        meal_cycle_order = ["breakfast", "lunch", "dinner", "dessert"]
        for index, recipe in enumerate(unassigned_recipes):
            meal_type = meal_cycle_order[index % 4]
            meal_recipe_ids[meal_type].append(str(recipe.id))

        def parse_and_sort_ids(raw_ids):
            """
            Convert a list of string IDs to integers, ignore invalid values,
            and return them sorted ascending.
            """
            if not raw_ids:
                return []
            numeric_ids = []
            for value in raw_ids:
                try:
                    numeric_ids.append(int(value))
                except ValueError:
                    # Ignore non-numeric values silently
                    continue
            return sorted(numeric_ids)

        # Parse and sort recipe IDs for each meal
        breakfast_ids = parse_and_sort_ids(meal_recipe_ids["breakfast"])
        lunch_ids = parse_and_sort_ids(meal_recipe_ids["lunch"])
        dinner_ids = parse_and_sort_ids(meal_recipe_ids["dinner"])
        dessert_ids = parse_and_sort_ids(meal_recipe_ids["dessert"])

        # Number of rows needed: enough to cover the longest meal list
        total_rows = max(
            len(breakfast_ids),
            len(lunch_ids),
            len(dinner_ids),
            len(dessert_ids),
            1,  # ensure at least one row is written
        )

        # Append all rows to the CSV file using the same menu_id and day
        with open(self.file_path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.headers)
            # Header is guaranteed to exist thanks to _ensure_file_exists
            for row_index in range(total_rows):
                row = {
                    "menu_id": str(next_menu_id),
                    "day": str(day),  # Always the same day for this customized menu
                    "breakfast_recipe_id": (
                        str(breakfast_ids[row_index]) if row_index < len(breakfast_ids) else "0"
                    ),
                    "lunch_recipe_id": (
                        str(lunch_ids[row_index]) if row_index < len(lunch_ids) else "0"
                    ),
                    "dinner_recipe_id": (
                        str(dinner_ids[row_index]) if row_index < len(dinner_ids) else "0"
                    ),
                    "dessert_recipe_id": (
                        str(dessert_ids[row_index]) if row_index < len(dessert_ids) else "0"
                    ),
                }
                writer.writerow(row)

        return next_menu_id
