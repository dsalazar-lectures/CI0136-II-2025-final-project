import unittest
import csv
import os
import tempfile
from src.Infrastructure.Menu.MenuRepository import MenuRepository
from src.Model.Menu.Menu import Menu
from src.Model.Menu.MenuDay import MenuDay


class TestMenuRepository(unittest.TestCase):

    def setUp(self):
        # Use a temporary directory so tests do not touch real CSV files
        self.temp_dir = tempfile.TemporaryDirectory()

        # Paths for normal and custom menus CSV inside the temp dir
        self.menus_csv_path = os.path.join(self.temp_dir.name, "menus.csv")
        self.custom_menus_csv_path = os.path.join(self.temp_dir.name, "custom_menus.csv")

        # Initialize normal menus CSV with headers
        headers = [
            "menu_id",
            "day",
            "breakfast_recipe_id",
            "lunch_recipe_id",
            "dinner_recipe_id",
            "dessert_recipe_id",
        ]

        with open(self.menus_csv_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

        # Initialize custom menus CSV with headers
        with open(self.custom_menus_csv_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

        self.repository = MenuRepository(
            csv_file_path=self.menus_csv_path,
            custom_csv_file_path=self.custom_menus_csv_path,
        )

    def tearDown(self):
        # Remove the entire temporary directory and its files
        self.temp_dir.cleanup()

    def test_create_menu_success(self):
        # Arrange
        menu = Menu(
            menu_id=1,
            daily_menus={1: MenuDay(101, 102, 103, 104)},
        )

        # Act
        result, message, status = self.repository.create_menu(menu)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(message, "Menu created successfully")
        self.assertEqual(status, 201)
        self.assertIsInstance(result, Menu)
        self.assertEqual(result.menu_id, 1)

    def test_get_menu_by_id_success(self):
        # Arrange
        menu = Menu(
            menu_id=1,
            daily_menus={
                1: MenuDay(101, 102, 103, 104),
                2: MenuDay(201, 202, 203, 204),
            },
        )
        self.repository.create_menu(menu)

        # Act
        result = self.repository.get_menu_by_id(1)

        # Assert
        self.assertIsNotNone(result)
        self.assertIsInstance(result, Menu)
        self.assertEqual(result.menu_id, 1)
        self.assertEqual(len(result.daily_menus), 2)

    def test_get_menu_by_id_not_found(self):
        # Act
        result = self.repository.get_menu_by_id(999)

        # Assert
        self.assertIsNone(result)

    def test_menu_exists(self):
        # Arrange
        menu = Menu(menu_id=1, daily_menus={1: MenuDay(101, 102, 103, 104)})
        self.repository.create_menu(menu)

        # Act & Assert
        self.assertTrue(self.repository.menu_exists(1))
        self.assertFalse(self.repository.menu_exists(999))

    def test_create_multiple_menus(self):
        # Arrange
        menu1 = Menu(menu_id=1, daily_menus={1: MenuDay(101, 102, 103, 104)})
        menu2 = Menu(menu_id=2, daily_menus={1: MenuDay(201, 202, 203, 204)})

        # Act
        result1, _, status1 = self.repository.create_menu(menu1)
        result2, _, status2 = self.repository.create_menu(menu2)

        # Assert
        self.assertEqual(status1, 201)
        self.assertEqual(status2, 201)
        self.assertIsNotNone(result1)
        self.assertIsNotNone(result2)

    def test_create_weekly_menu(self):
        # Arrange
        daily_menus = {
            i: MenuDay(i * 100, i * 100 + 1, i * 100 + 2, i * 100 + 3)
            for i in range(1, 8)
        }
        menu = Menu(menu_id=1, daily_menus=daily_menus)

        # Act
        result, message, status = self.repository.create_menu(menu)

        # Assert
        self.assertEqual(status, 201)
        self.assertIsNotNone(result)
        self.assertEqual(len(result.daily_menus), 7)

        # Verify retrieval
        retrieved = self.repository.get_menu_by_id(1)
        self.assertEqual(len(retrieved.daily_menus), 7)

    def test_delete_menu_not_exists(self):
        # Act
        result, message, status = self.repository.delete_menu(999)

        # Assert
        self.assertIsNone(result)
        self.assertEqual(message, "Menu does not exist")
        self.assertEqual(status, 404)

    def test_delete_menu_success(self):
        # Arrange
        menu = Menu(
            menu_id=1,
            daily_menus={
                1: MenuDay(101, 102, 103, 104),
                2: MenuDay(201, 202, 203, 204),
            },
        )
        self.repository.create_menu(menu)

        # Act
        result, message, status = self.repository.delete_menu(1)

        # Assert
        self.assertTrue(result)
        self.assertEqual(message, "Menu deleted successfully")
        self.assertEqual(status, 200)
        self.assertFalse(self.repository.menu_exists(1))
        self.assertIsNone(self.repository.get_menu_by_id(1))

    def test_delete_menu_removes_all_days(self):
        # Arrange - Create a multi-day menu
        menu = Menu(
            menu_id=1,
            daily_menus={
                1: MenuDay(101, 102, 103, 104),
                2: MenuDay(201, 202, 203, 204),
                3: MenuDay(301, 302, 303, 304),
            },
        )
        self.repository.create_menu(menu)

        # Act
        result, message, status = self.repository.delete_menu(1)

        # Assert
        self.assertTrue(result)
        self.assertEqual(status, 200)
        # Verify all days were removed
        retrieved = self.repository.get_menu_by_id(1)
        self.assertIsNone(retrieved)

    def test_list_menus_empty(self):
        # Act
        result = self.repository.list_menus()

        # Assert
        self.assertEqual(result, [])

    def test_list_menus_single_menu(self):
        # Arrange
        menu = Menu(
            menu_id=1,
            daily_menus={
                1: MenuDay(101, 102, 103, 104),
                2: MenuDay(201, 202, 203, 204),
            },
        )
        self.repository.create_menu(menu)

        # Act
        result = self.repository.list_menus()

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["menu_id"], 1)
        self.assertEqual(len(result[0]["daily_menus"]), 2)

    def test_list_menus_multiple(self):
        # Arrange
        menu1 = Menu(menu_id=1, daily_menus={1: MenuDay(101, 102, 103, 104)})
        menu2 = Menu(
            menu_id=2,
            daily_menus={
                1: MenuDay(201, 202, 203, 204),
                2: MenuDay(211, 212, 213, 214),
            },
        )
        menu3 = Menu(
            menu_id=3,
            daily_menus={
                1: MenuDay(301, 302, 303, 304),
                2: MenuDay(311, 312, 313, 314),
                3: MenuDay(321, 322, 323, 324),
            },
        )
        self.repository.create_menu(menu1)
        self.repository.create_menu(menu2)
        self.repository.create_menu(menu3)

        # Act
        result = self.repository.list_menus()

        # Assert
        self.assertEqual(len(result), 3)
        menu_ids = [m["menu_id"] for m in result]
        self.assertEqual(sorted(menu_ids), [1, 2, 3])

    def test_delete_from_multiple_menus(self):
        # Arrange
        menu1 = Menu(menu_id=1, daily_menus={1: MenuDay(101, 102, 103, 104)})
        menu2 = Menu(menu_id=2, daily_menus={1: MenuDay(201, 202, 203, 204)})
        menu3 = Menu(menu_id=3, daily_menus={1: MenuDay(301, 302, 303, 304)})
        self.repository.create_menu(menu1)
        self.repository.create_menu(menu2)
        self.repository.create_menu(menu3)

        # Act - Delete menu 2
        self.repository.delete_menu(2)

        # Assert
        self.assertTrue(self.repository.menu_exists(1))
        self.assertFalse(self.repository.menu_exists(2))
        self.assertTrue(self.repository.menu_exists(3))

        # Verify list_menus reflects deletion
        result = self.repository.list_menus()
        self.assertEqual(len(result), 2)
        menu_ids = [m["menu_id"] for m in result]
        self.assertIn(1, menu_ids)
        self.assertNotIn(2, menu_ids)
        self.assertIn(3, menu_ids)


if __name__ == "__main__":
    unittest.main()
