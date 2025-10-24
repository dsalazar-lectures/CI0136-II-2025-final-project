import unittest
from unittest.mock import patch
from src.Application.Recipes import recipe_service

class DummyRecipe:
    def __init__(self, id, name, categories, ingredients, author):
        self.id = id
        self.name = name
        self.categories = categories
        self.ingredients = ingredients
        self.author = author
    def to_dict(self):
        return {"id": self.id, "name": self.name, "categories": self.categories, "ingredients": self.ingredients, "author": self.author}

class DummyRepo:
    def find_by_category(self, category):
        return [DummyRecipe(1, "recipe1", [category], ["ingredient1"], "user1")]

class RecipeServiceTestCase(unittest.TestCase):
    def setUp(self):
        patcher = patch.object(recipe_service, "recipe_repository", DummyRepo())
        self.addCleanup(patcher.stop)
        self.mock_repo = patcher.start()

    def test_get_recipes_by_category(self):
        recipes = recipe_service.get_recipes_by_category("category1")
        self.assertEqual(recipes[0].categories, ["category1"])

if __name__ == "__main__":
    unittest.main()
