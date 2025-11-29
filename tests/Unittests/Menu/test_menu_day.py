import unittest
from src.Model.Menu.MenuDay import MenuDay


class TestMenuDay(unittest.TestCase):

    def test_create_menu_day_success(self):
        # Arrange & Act
        menu_day = MenuDay(
            breakfast_recipe_id=101,
            lunch_recipe_id=102,
            dinner_recipe_id=103,
            dessert_recipe_id=104,
        )

        # Assert
        self.assertEqual(menu_day.breakfast, 101)
        self.assertEqual(menu_day.lunch, 102)
        self.assertEqual(menu_day.dinner, 103)
        self.assertEqual(menu_day.dessert, 104)

    def test_to_dict_returns_correct_structure(self):
        # Arrange
        menu_day = MenuDay(
            breakfast_recipe_id=201,
            lunch_recipe_id=202,
            dinner_recipe_id=203,
            dessert_recipe_id=204,
        )

        # Act
        result = menu_day.to_dict()

        # Assert
        expected = {
            "breakfast": 201,
            "lunch": 202,
            "dinner": 203,
            "dessert": 204,
        }
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
