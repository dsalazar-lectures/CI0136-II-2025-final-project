import unittest
from tests.Mocks.Recipes.mock_recipe_repo import MockRecipe
from src.Application.Menu import menu_service


class MenuServiceTestCase(unittest.TestCase):
    def test_generate_menus_happy_path(self):
        recipes = [MockRecipe(1, "recipe1", ["category1"]), MockRecipe(2, "recipe2", ["category2"])]
        menus = menu_service.generate_menus(recipes, 3)
        self.assertEqual(len(menus), 3)
        names = [m["recipe"]["name"] for m in menus]
        self.assertEqual(names, ["recipe1", "recipe2", "recipe1"])
        self.assertEqual(menus[0]["menu"], "Menú #1")

    def test_empty_recipes_returns_empty(self):
        self.assertEqual(menu_service.generate_menus([], 5), [])

    def test_count_zero_returns_empty(self):
        recipes = [MockRecipe(1, "recipe1", ["category1"])]
        # current implementation returns empty list for count 0
        self.assertEqual(menu_service.generate_menus(recipes, 0), [])

    def test_non_int_count_raises(self):
        recipes = [MockRecipe(1, "recipe1", ["category1"])]
        with self.assertRaises(TypeError):
            # passing a string should raise when used in range()
            menu_service.generate_menus(recipes, "3")

    def test_recipe_without_to_dict_raises(self):
        class Bad:
            pass

        with self.assertRaises(AttributeError):
            menu_service.generate_menus([Bad()], 1)


if __name__ == "__main__":
    unittest.main()
