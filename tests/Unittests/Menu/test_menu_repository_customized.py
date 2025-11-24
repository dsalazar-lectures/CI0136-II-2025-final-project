import unittest
import os
import csv
import tempfile
from unittest.mock import patch

from src.Infrastructure.Menu.MenuRepository import MenuRepository
from src.Database.Menu.MenuCSV import MenuCSV
from src.Model.Menu.Menu import Menu
from tests.Mocks.Menu.mock_customized_menu import FakeRecipe


class TestMenuRepositoryCustomizedMenu(unittest.TestCase):
    def setUp(self):
        # Use a temporary directory so tests don't touch real CSV files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.menus_csv_path = os.path.join(self.temp_dir.name, "menus.csv")
        self.custom_menus_csv_path = os.path.join(
            self.temp_dir.name, "custom_menus.csv"
        )

        # Instantiate repository with test CSV paths
        self.repo = MenuRepository(
            csv_file_path=self.menus_csv_path,
            custom_csv_file_path=self.custom_menus_csv_path,
        )

    def tearDown(self):
        # Clean up temporary directory and files
        self.temp_dir.cleanup()

    def test_create_customized_menu_creates_menu_and_persists_in_custom_csv(self):
        # Arrange: build a small set of fake recipes
        recipes = [
            FakeRecipe(
                "Desayuno 1",
                ["Huevo", "Pan"],
                ["desayuno"],
                rating=4,
            ),
            FakeRecipe(
                "Almuerzo 1",
                ["Arroz", "Pollo"],
                ["almuerzo"],
                rating=5,
            ),
            FakeRecipe(
                "Cena 1",
                ["Pasta", "Tomate"],
                ["cena"],
                rating=3,
            ),
        ]

        # Act: create customized menu
        menu_obj, msg, status = self.repo.create_customized_menu(recipes)

        # Assert: repository contract
        self.assertEqual(status, 201)
        self.assertEqual(msg, "Customized menu created")
        self.assertIsNotNone(menu_obj)
        self.assertIsInstance(menu_obj, Menu)
        self.assertIsInstance(menu_obj.menu_id, int)

        # Assert: verify CSV was written with this menu_id
        with open(self.custom_menus_csv_path, "r", newline="") as f:
            rows = list(csv.DictReader(f))

        # There should be at least one data row
        self.assertGreaterEqual(len(rows), 1)

        # All rows must share the same menu_id as the returned Menu object
        menu_ids_in_file = {int(row["menu_id"]) for row in rows}
        self.assertEqual(menu_ids_in_file, {menu_obj.menu_id})

        # All rows should have a valid day (in this case day=1)
        days_in_file = {row["day"] for row in rows}
        self.assertEqual(days_in_file, {"1"})

    @patch.object(MenuCSV, "get_menu_by_id", return_value=None)
    def test_create_customized_menu_returns_error_when_menu_not_found(
        self, mock_get_menu_by_id
    ):
        # Arrange: at least one recipe so save_customized is called
        recipes = [
            FakeRecipe(
                "Any recipe",
                ["Ingrediente"],
                ["almuerzo"],
                rating=3,
            )
        ]

        # Act: force get_menu_by_id to fail (return None)
        menu_obj, msg, status = self.repo.create_customized_menu(recipes)

        # Assert: repository signals error correctly
        self.assertIsNone(menu_obj)
        self.assertEqual(msg, "Error creating customized menu")
        self.assertEqual(status, 500)


if __name__ == "__main__":
    unittest.main()