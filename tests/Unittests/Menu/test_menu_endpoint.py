import unittest
from unittest.mock import patch
from flask import Flask
from types import SimpleNamespace
from src.Application.Menu import MenuUseCase
from src.API.Menu.menuRoutes import menu_bp
from tests.Mocks.Recipes.mock_recipe_repo import MockRecipe


class MenuEndpointTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(menu_bp, url_prefix="/api")
        self.client = app.test_client()

    @patch("src.Application.Recipes.recipe_service.get_recipes_by_category")
    def test_get_menu_returns_empty_list_when_recipes_repo_empty(
        self, mock_get_recipes
    ):
        mock_get_recipes.return_value = []
        response = self.client.get("/api/menu?category=unknown")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, [{}])

    @patch("src.Application.Recipes.recipe_service.get_random_recipe_by_category")
    def test_get_menu_returns_one_random_recipe(self, mock_get_random_recipe):
        recipe = MockRecipe(1, "recipe1", ["category1", "category2"])
        mock_get_random_recipe.return_value = recipe
        response = self.client.get("/api/menu?category=category1")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "recipe1")

    @patch("src.Application.Recipes.recipe_service.get_random_recipe_by_category")
    def test_get_menu_empty_category(self, mock_get_random_recipe):
        mock_get_random_recipe.return_value = None
        response = self.client.get("/api/menu?category=unknown")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, [{}])

    @patch("src.Application.Recipes.recipe_service.get_random_recipe_by_category")
    def test_get_menu_category_filter(self, mock_get_random_recipe):
        recipe = MockRecipe(2, "recipe2", ["category2"])
        mock_get_random_recipe.return_value = recipe
        response = self.client.get("/api/menu?category=category2")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "recipe2")

    def test_get_menu_emailPdf_invalid_address(self):
        response = MenuUseCase.emailPdf(1, "test.gmail.com")
        self.assertEqual(response, 400)

    def test_customized_menu_get_requires_user_id(self):
        response = self.client.get("/api/menu/customized")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data, {"error": "user_id requerido"})

    @patch("src.API.Menu.menuRoutes.customized_service")
    @patch("src.API.Menu.menuRoutes.profile_service")
    def test_customized_menu_get_returns_recipes(
        self, mock_profile_service, mock_customized_service
    ):
        fake_profile = SimpleNamespace(favorite_foods=["tomate", "queso"])
        mock_profile_service.get_profile.return_value = fake_profile

        fake_recipes = [
            MockRecipe(1, "Custom Recipe 1", ["almuerzo"]),
            MockRecipe(2, "Custom Recipe 2", ["almuerzo"]),
        ]
        mock_customized_service.recommend_by_favorites.return_value = fake_recipes

        response = self.client.get("/api/menu/customized?user_id=1&category=almuerzo")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("recipes", data)
        self.assertIsInstance(data["recipes"], list)
        self.assertEqual(len(data["recipes"]), 2)
        self.assertEqual(data["recipes"][0]["name"], "Custom Recipe 1")
        self.assertNotIn("menu_id", data)

    @patch("src.API.Menu.menuRoutes.MenuRepository")
    @patch("src.API.Menu.menuRoutes.customized_service")
    @patch("src.API.Menu.menuRoutes.profile_service")
    def test_customized_menu_post_creates_customized_menu(
        self, mock_profile_service, mock_customized_service, mock_menu_repo_cls
    ):
        fake_profile = SimpleNamespace(favorite_foods=["tomate"])
        mock_profile_service.get_profile.return_value = fake_profile

        fake_recipes = [MockRecipe(1, "Custom Recipe 1", ["almuerzo"])]
        mock_customized_service.recommend_by_favorites.return_value = fake_recipes

        mock_repo_instance = mock_menu_repo_cls.return_value
        fake_menu_obj = SimpleNamespace(menu_id=123)
        mock_repo_instance.create_customized_menu.return_value = (
            fake_menu_obj,
            "Customized menu created",
            201,
        )

        response = self.client.post("/api/menu/customized?user_id=1&category=almuerzo")

        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("recipes", data)
        self.assertEqual(len(data["recipes"]), 1)
        self.assertEqual(data["menu_id"], 123)
        self.assertEqual(data["message"], "Customized menu created")

        mock_repo_instance.create_customized_menu.assert_called_once()

    @patch("src.API.Menu.menuRoutes.profile_service")
    def test_customized_menu_post_profile_not_found(self, mock_profile_service):
        mock_profile_service.get_profile.return_value = None

        response = self.client.post(
            "/api/menu/customized?user_id=999&category=almuerzo"
        )

        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data, {"error": "Perfil no encontrado"})


if __name__ == "__main__":
    unittest.main()
