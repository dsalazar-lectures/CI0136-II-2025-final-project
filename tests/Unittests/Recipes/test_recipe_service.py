import unittest
from unittest.mock import patch
from src.Application.Recipes import recipe_service
from tests.Mocks.Recipes.mock_recipe import MockRecipe
from tests.Mocks.Recipes.mock_recipe_repo import MockRecipeRepo


class RecipeServiceTestCase(unittest.TestCase):
    def setUp(self):
        dummy_repo = MockRecipeRepo(
            recipes=[MockRecipe(1, "recipe1", ["category1"], ["ingredient1"], "user1")],
        )
        patcher = patch.object(recipe_service, "recipe_repository", dummy_repo)
        self.addCleanup(patcher.stop)
        self.mock_repo = patcher.start()

    def test_get_random_recipe_by_category(self):
        recipe = recipe_service.get_random_recipe_by_category("category1")
        self.assertIsNotNone(recipe)
        self.assertEqual(recipe.categories, ["category1"])

    def test_get_random_recipe_by_category_none(self):
        # Patch repo to return empty list
        self.mock_repo._recipes = []
        recipe = recipe_service.get_random_recipe_by_category("category1")
        self.assertIsNone(recipe)


if __name__ == "__main__":
    unittest.main()
