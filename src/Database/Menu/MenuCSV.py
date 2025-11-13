import csv
import os
from src.Model.Menu.Menu import Menu

class MenuCSV:
    def __init__(self, file_path):
        self.file_path = file_path
        # Ensure the CSV file exists and has headers
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ["menu_id", "recipes"]
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
                ids = [int(row["menu_id"]) for row in reader if row["menu_id"].isdigit()]
                if ids:
                    next_id = max(ids) + 1

        new_menu = {
            "menu_id": str(next_id),
            "recipes": ";".join(menu.recipes),
        }

        # Appends new menu to CSV file
        with open(self.file_path, "a", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "menu_id",
                    "recipes",
                ],
            )
            writer.writerow(new_menu)

        return new_menu

    def get_menu_by_id(self, menu_id: int) -> dict:
        if not os.path.exists(self.file_path):
            return None
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for csv_row in reader:
                if csv_row["menu_id"] == str(menu_id):
                    return csv_row
        return None
