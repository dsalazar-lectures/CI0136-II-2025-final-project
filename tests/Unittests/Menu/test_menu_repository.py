import unittest
import csv
import os
import tempfile
from src.Infrastructure.Menu.MenuRepository import MenuRepository
from src.Model.Menu.Menu import Menu
from src.Model.Menu.MenuDay import MenuDay


class TestMenuRepository(unittest.TestCase):

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

        self.repository = MenuRepository(self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

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

    def test_delete_menu_not_exists(self):
        # Act
        result, message, status = self.repository.delete_menu(999)

        # Assert
        self.assertIsNone(result)
        self.assertEqual(message, "Menu does not exist")
        self.assertEqual(status, 404)

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


if __name__ == "__main__":
    unittest.main()
