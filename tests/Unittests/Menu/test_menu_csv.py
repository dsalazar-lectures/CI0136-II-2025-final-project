import unittest
import csv
import os
import tempfile
from src.Database.Menu.MenuCSV import MenuCSV
from src.Model.Menu.Menu import Menu
from src.Model.Menu.MenuDay import MenuDay


class TestMenuCSV(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix="_test_menus.csv"
        )
        self.temp_file.close()

        with open(self.temp_file.name, "w", newline="") as file:
            writer = csv.writer(file)
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

        self.menu_csv = MenuCSV(self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_create_single_day_menu(self):
        # Arrange
        menu = Menu(
            menu_id=1,
            daily_menus={1: MenuDay(101, 102, 103, 104)},
        )

        # Act
        result = self.menu_csv.create_menu(menu)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(int(result["menu_id"]), 1)
        self.assertEqual(len(result["daily_menus"]), 1)

        # Verify file content
        with open(self.temp_file.name, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)  # Header + 1 data row

    def test_create_multi_day_menu(self):
        # Arrange
        menu = Menu(
            menu_id=1,
            daily_menus={
                1: MenuDay(101, 102, 103, 104),
                2: MenuDay(201, 202, 203, 204),
                3: MenuDay(301, 302, 303, 304),
            },
        )

        # Act
        result = self.menu_csv.create_menu(menu)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(int(result["menu_id"]), 1)
        self.assertEqual(len(result["daily_menus"]), 3)

        # Verify file content
        with open(self.temp_file.name, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 4)  # Header + 3 data rows

    def test_get_menu_by_id_single_day(self):
        # Arrange
        menu = Menu(menu_id=1, daily_menus={1: MenuDay(101, 102, 103, 104)})
        self.menu_csv.create_menu(menu)

        # Act
        result = self.menu_csv.get_menu_by_id(1)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["menu_id"], 1)
        self.assertEqual(len(result["daily_menus"]), 1)
        self.assertEqual(result["daily_menus"][1]["breakfast_recipe_id"], 101)
        self.assertEqual(result["daily_menus"][1]["lunch_recipe_id"], 102)
        self.assertEqual(result["daily_menus"][1]["dinner_recipe_id"], 103)
        self.assertEqual(result["daily_menus"][1]["dessert_recipe_id"], 104)

    def test_get_menu_by_id_multi_day(self):
        # Arrange
        menu = Menu(
            menu_id=1,
            daily_menus={
                1: MenuDay(101, 102, 103, 104),
                2: MenuDay(201, 202, 203, 204),
            },
        )
        self.menu_csv.create_menu(menu)

        # Act
        result = self.menu_csv.get_menu_by_id(1)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["menu_id"], 1)
        self.assertEqual(len(result["daily_menus"]), 2)
        self.assertEqual(result["daily_menus"][1]["breakfast_recipe_id"], 101)
        self.assertEqual(result["daily_menus"][2]["breakfast_recipe_id"], 201)

    def test_get_menu_by_id_not_found(self):
        # Act
        result = self.menu_csv.get_menu_by_id(999)

        # Assert
        self.assertIsNone(result)

    def test_menu_exists(self):
        # Arrange
        menu = Menu(menu_id=1, daily_menus={1: MenuDay(101, 102, 103, 104)})
        self.menu_csv.create_menu(menu)

        # Act & Assert
        self.assertTrue(self.menu_csv.menu_exists(1))
        self.assertFalse(self.menu_csv.menu_exists(999))

    def test_create_multiple_menus(self):
        # Arrange
        menu1 = Menu(menu_id=1, daily_menus={1: MenuDay(101, 102, 103, 104)})
        menu2 = Menu(
            menu_id=2,
            daily_menus={
                1: MenuDay(201, 202, 203, 204),
                2: MenuDay(211, 212, 213, 214),
            },
        )

        # Act
        self.menu_csv.create_menu(menu1)
        self.menu_csv.create_menu(menu2)

        # Assert
        result1 = self.menu_csv.get_menu_by_id(1)
        result2 = self.menu_csv.get_menu_by_id(2)

        self.assertIsNotNone(result1)
        self.assertIsNotNone(result2)
        self.assertEqual(len(result1["daily_menus"]), 1)
        self.assertEqual(len(result2["daily_menus"]), 2)

    def test_auto_increment_menu_id(self):
        # Arrange
        menu1 = Menu(menu_id=999, daily_menus={1: MenuDay(101, 102, 103, 104)})
        menu2 = Menu(menu_id=888, daily_menus={1: MenuDay(201, 202, 203, 204)})

        # Act
        result1 = self.menu_csv.create_menu(menu1)
        result2 = self.menu_csv.create_menu(menu2)

        # Assert - IDs should be auto-incremented (1, 2)
        self.assertEqual(int(result1["menu_id"]), 1)
        self.assertEqual(int(result2["menu_id"]), 2)

    def test_weekly_menu_seven_days(self):
        # Arrange
        daily_menus = {
            i: MenuDay(i * 100, i * 100 + 1, i * 100 + 2, i * 100 + 3)
            for i in range(1, 8)
        }
        menu = Menu(menu_id=1, daily_menus=daily_menus)

        # Act
        self.menu_csv.create_menu(menu)
        result = self.menu_csv.get_menu_by_id(1)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(len(result["daily_menus"]), 7)
        for day in range(1, 8):
            self.assertIn(day, result["daily_menus"])
            self.assertEqual(
                result["daily_menus"][day]["breakfast_recipe_id"], day * 100
            )

    def test_nonexistent_file_provided(self):
        # Arrange
        nonexistent_path = "not_a_file_that_exists.csv"

        # Ensure file doesn't exist before test
        if os.path.exists(nonexistent_path):
            os.unlink(nonexistent_path)

        # Act
        menu_csv_no_file = MenuCSV(nonexistent_path)

        # Assert - File should be created with headers
        self.assertTrue(os.path.exists(nonexistent_path))

        # Verify headers were written
        with open(nonexistent_path, "r") as f:
            reader = csv.reader(f)
            headers = next(reader)
            self.assertEqual(
                headers,
                [
                    "menu_id",
                    "day",
                    "breakfast_recipe_id",
                    "lunch_recipe_id",
                    "dinner_recipe_id",
                    "dessert_recipe_id",
                ],
            )

        # Cleanup
        if os.path.exists(nonexistent_path):
            os.unlink(nonexistent_path)


if __name__ == "__main__":
    unittest.main()
