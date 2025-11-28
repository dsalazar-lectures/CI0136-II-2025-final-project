import unittest
from unittest.mock import patch
from flask import Flask
from types import SimpleNamespace
import os
from src.Application.Menu import MenuUseCase
from src.API.Menu.menuRoutes import menu_bp
from src.Model.Menu.Menu import Menu
from src.Model.Menu.MenuDay import MenuDay

from tests.Mocks.Recipes.mock_recipe_repo import MockRecipe


class MenuEndpointTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(menu_bp, url_prefix="/api")
        self.client = app.test_client()

    def tearDown(self):
        # profiles
        if os.path.exists("profiles.csv"):
            os.remove("profiles.csv")

        # menus
        menus_path = os.path.join("src", "Database", "Menu", "menus.csv")
        if os.path.exists(menus_path):
            os.remove(menus_path)

        # customized menus
        custom_menus_path = os.path.join("src", "Database", "Menu", "custom_menus.csv")
        if os.path.exists(custom_menus_path):
            os.remove(custom_menus_path)

        # API recipes
        api_recipes_path = os.path.join("src", "Database", "Recipes", "APIRecipes.csv")
        if os.path.exists(api_recipes_path):
            os.remove(api_recipes_path)

    @patch("src.Application.Menu.MenuUseCase.generateRandomMenu")
    def test_get_menu_returns_new_menu_structure(self, mock_generate_random_menu):
        # Create a Menu with two days (keys are ints, will become strings in JSON)
        daily_menus = {
            1: MenuDay(101, 102, 103, 104),
            2: MenuDay(201, 202, 203, 204),
        }
        menu_obj = Menu(menu_id=42, daily_menus=daily_menus)
        mock_generate_random_menu.return_value = menu_obj

        response = self.client.get("/api/menu")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Top-level keys
        self.assertIn("menu_id", data)
        self.assertIn("daily_menus", data)
        self.assertEqual(data["menu_id"], 42)

        # daily_menus keys should start at '1' and be strings
        keys = list(data["daily_menus"].keys())
        self.assertEqual(keys, ["1", "2"])

        # Each day should have MenuDay structure
        day1 = data["daily_menus"]["1"]
        self.assertEqual(day1["breakfast"], 101)
        self.assertEqual(day1["lunch"], 102)
        self.assertEqual(day1["dinner"], 103)
        self.assertEqual(day1["dessert"], 104)

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
