import os
import unittest
from unittest.mock import patch
from flask import Flask
from tests.Mocks.Menu.mock_menu_service import MockMenuService
from tests.Mocks.Menu.mock_menu_repository import MockMenuRepository

API_RECIPES_PATH = os.path.join("src", "Database", "Recipes", "APIRecipes.csv")


class GenerateMenusTestCase(unittest.TestCase):
    def setUp(self):
        # Mock all repository and service instantiations before importing
        with patch("src.Infrastructure.Menu.MenuRepository.MenuRepository"), patch(
            "src.Infrastructure.Profiles.ProfileRepository.ProfileRepository"
        ), patch(
            "src.Application.Menu.CustomizedMenuService.CustomizedMenuService"
        ), patch(
            "src.Application.Profiles.Services.ProfileApplicationService.ProfileApplicationService"
        ):
            from src.API.Menu.menuRoutes import menu_bp

            app = Flask(__name__)
            app.register_blueprint(menu_bp, url_prefix="/api")
            self.client = app.test_client()

    def tearDown(self):
        if os.path.exists(API_RECIPES_PATH):
            os.remove(API_RECIPES_PATH)

    @patch("src.Application.Menu.menu_service.generate_menus")
    @patch("src.API.Menu.menuRoutes.menu_repository")
    def test_generate_menus_with_valid_count(
        self, mock_menu_repository, mock_generate_menus
    ):
        # Use mock objects
        mock_repo = MockMenuRepository()
        mock_menu_repository.create_menu = mock_repo.create_menu

        menu, missing_categories, menu_details = MockMenuService.generate_valid_menu(2)
        mock_generate_menus.return_value = (menu, missing_categories, menu_details)

        # Make request
        response = self.client.get("/api/menu/2")
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        # Verify response structure
        self.assertIn("menu_id", data)
        self.assertIn("daily_menus", data)
        self.assertEqual(data["menu_id"], 1)
        self.assertEqual(len(data["daily_menus"]), 2)

        # Verify day 1
        day1 = data["daily_menus"][0]
        self.assertEqual(day1["day"], 1)
        self.assertEqual(day1["breakfast"]["name"], "Pancakes")
        self.assertEqual(day1["lunch"]["name"], "Pasta")
        self.assertEqual(day1["dinner"]["name"], "Salmón")
        self.assertEqual(day1["dessert"]["name"], "Flan")

    @patch("src.Application.Menu.menu_service.generate_menus")
    def test_generate_menus_with_invalid_count(self, mock_generate_menus):
        # Test with count < 1
        response = self.client.get("/api/menu/0")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertIn("número entero positivo", data["error"])

        # Verify generate_menus was not called
        mock_generate_menus.assert_not_called()

    @patch("src.Application.Menu.menu_service.generate_menus")
    def test_generate_menus_with_missing_categories(self, mock_generate_menus):
        # Use mock service
        menu, missing_categories, menu_details = (
            MockMenuService.generate_menu_with_missing_categories(
                ["desayuno", "postre"]
            )
        )
        mock_generate_menus.return_value = (menu, missing_categories, menu_details)

        response = self.client.get("/api/menu/3")
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertIn("desayuno", data["error"])
        self.assertIn("postre", data["error"])

    @patch("src.Application.Menu.menu_service.generate_menus")
    @patch("src.API.Menu.menuRoutes.menu_repository.create_menu")
    def test_generate_menus_repository_error(
        self, mock_create_menu, mock_generate_menus
    ):
        # Use mock service for valid menu
        menu, missing_categories, menu_details = MockMenuService.generate_valid_menu(1)
        mock_generate_menus.return_value = (menu, missing_categories, menu_details)

        # Mock repository error
        mock_create_menu.return_value = (None, "Error saving menu", 500)

        response = self.client.get("/api/menu/1")
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Error saving menu")


if __name__ == "__main__":
    unittest.main()
