import unittest
from unittest.mock import patch
from src.Application.Recipes import recipe_service
from tests.Mocks.Recipes.mock_recipe import MockRecipeRepo
from tests.Mocks.Recipes.mock_recipe_repo import MockRecipe

class RecipeServiceTestCase(unittest.TestCase):
    def setUp(self):
        dummy_repo = MockRecipeRepo(recipes=[MockRecipe(1, "recipe1", ["category1"], ["ingredient1"], "user1")])
        patcher = patch.object(recipe_service, "recipe_repository", dummy_repo)
        self.addCleanup(patcher.stop)
        self.mock_repo = patcher.start()

    def test_get_recipes_by_category(self):
        recipes = recipe_service.get_recipes_by_category("category1")
        self.assertEqual(recipes[0].categories, ["category1"])

if __name__ == "__main__":
    unittest.main()
