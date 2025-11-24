import unittest
from src.Model.Menu.Menu import Menu
from src.Model.Menu.MenuDay import MenuDay


class TestMenu(unittest.TestCase):

    def test_create_single_day_menu(self):
        # Arrange
        menu_day = MenuDay(
            breakfast_recipe_id=101,
            lunch_recipe_id=102,
            dinner_recipe_id=103,
            dessert_recipe_id=104,
        )

        # Act
        menu = Menu(menu_id=1, daily_menus={1: menu_day})

        # Assert
        self.assertEqual(menu.menu_id, 1)
        self.assertEqual(len(menu.daily_menus), 1)
        self.assertIn(1, menu.daily_menus)
        self.assertEqual(menu.daily_menus[1].breakfast, 101)

    def test_create_multi_day_menu(self):
        # Arrange
        daily_menus = {
            1: MenuDay(101, 102, 103, 104),
            2: MenuDay(201, 202, 203, 204),
            3: MenuDay(301, 302, 303, 304),
        }

        # Act
        menu = Menu(menu_id=2, daily_menus=daily_menus)

        # Assert
        self.assertEqual(menu.menu_id, 2)
        self.assertEqual(len(menu.daily_menus), 3)
        self.assertIn(1, menu.daily_menus)
        self.assertIn(2, menu.daily_menus)
        self.assertIn(3, menu.daily_menus)

    def test_to_dict_single_day(self):
        # Arrange
        menu_day = MenuDay(101, 102, 103, 104)
        menu = Menu(menu_id=1, daily_menus={1: menu_day})

        # Act
        result = menu.to_dict()

        # Assert
        expected = {
            "menu_id": 1,
            "daily_menus": {
                1: {"breakfast": 101, "lunch": 102, "dinner": 103, "dessert": 104}
            },
        }
        self.assertEqual(result, expected)

    def test_to_dict_multi_day(self):
        # Arrange
        daily_menus = {
            1: MenuDay(101, 102, 103, 104),
            2: MenuDay(201, 202, 203, 204),
        }
        menu = Menu(menu_id=5, daily_menus=daily_menus)

        # Act
        result = menu.to_dict()

        # Assert
        self.assertEqual(result["menu_id"], 5)
        self.assertEqual(len(result["daily_menus"]), 2)
        self.assertEqual(result["daily_menus"][1]["breakfast"], 101)
        self.assertEqual(result["daily_menus"][2]["lunch"], 202)

    def test_empty_daily_menus(self):
        # Arrange & Act
        menu = Menu(menu_id=3, daily_menus={})

        # Assert
        self.assertEqual(menu.menu_id, 3)
        self.assertEqual(len(menu.daily_menus), 0)
        self.assertEqual(menu.to_dict()["daily_menus"], {})

    def test_weekly_menu_seven_days(self):
        # Arrange
        daily_menus = {
            i: MenuDay(i * 100, i * 100 + 1, i * 100 + 2, i * 100 + 3)
            for i in range(1, 8)
        }

        # Act
        menu = Menu(menu_id=10, daily_menus=daily_menus)

        # Assert
        self.assertEqual(len(menu.daily_menus), 7)
        for day in range(1, 8):
            self.assertIn(day, menu.daily_menus)


if __name__ == "__main__":
    unittest.main()
