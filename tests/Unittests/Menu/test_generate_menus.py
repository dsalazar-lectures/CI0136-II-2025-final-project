import unittest
from unittest.mock import patch, MagicMock
from flask import Flask


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

    @patch("src.Application.Menu.menu_service.generate_menus")
    @patch("src.API.Menu.menuRoutes.menu_repository.create_menu")
    def test_generate_menus_with_valid_count(
        self, mock_create_menu, mock_generate_menus
    ):
        # Mock menu object
        mock_menu = MagicMock()
        mock_menu.menu_id = 1

        # Mock menu details with full recipe information
        menu_details = [
            {
                "day": 1,
                "breakfast": {"id": 1, "name": "Pancakes", "categories": ["desayuno"]},
                "lunch": {
                    "id": 2,
                    "name": "Pasta con Tomate",
                    "categories": ["almuerzo"],
                },
                "dinner": {"id": 3, "name": "Salmón al Horno", "categories": ["cena"]},
                "dessert": {
                    "id": 4,
                    "name": "Flan de Caramelo",
                    "categories": ["postre"],
                },
            },
            {
                "day": 2,
                "breakfast": {
                    "id": 5,
                    "name": "Gallo Pinto",
                    "categories": ["desayuno"],
                },
                "lunch": {
                    "id": 6,
                    "name": "Arroz con Pollo",
                    "categories": ["almuerzo"],
                },
                "dinner": {"id": 7, "name": "Tacos de Carne", "categories": ["cena"]},
                "dessert": {"id": 8, "name": "Tiramisú", "categories": ["postre"]},
            },
        ]

        # Configure mocks
        mock_generate_menus.return_value = (mock_menu, None, menu_details)
        mock_saved_menu = MagicMock()
        mock_saved_menu.menu_id = 1
        mock_create_menu.return_value = (
            mock_saved_menu,
            "Menu created successfully",
            201,
        )

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
        self.assertEqual(day1["lunch"]["name"], "Pasta con Tomate")
        self.assertEqual(day1["dinner"]["name"], "Salmón al Horno")
        self.assertEqual(day1["dessert"]["name"], "Flan de Caramelo")

        # Verify day 2
        day2 = data["daily_menus"][1]
        self.assertEqual(day2["day"], 2)
        self.assertEqual(day2["breakfast"]["name"], "Gallo Pinto")
        self.assertEqual(day2["lunch"]["name"], "Arroz con Pollo")
        self.assertEqual(day2["dinner"]["name"], "Tacos de Carne")
        self.assertEqual(day2["dessert"]["name"], "Tiramisú")

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
        # Mock missing categories
        missing_categories = ["desayuno", "postre"]
        mock_generate_menus.return_value = (None, missing_categories, None)

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
        # Mock successful menu generation
        mock_menu = MagicMock()
        menu_details = [
            {
                "day": 1,
                "breakfast": {"id": 1, "name": "Pancakes"},
                "lunch": {"id": 2, "name": "Pasta"},
                "dinner": {"id": 3, "name": "Salmón"},
                "dessert": {"id": 4, "name": "Flan"},
            }
        ]
        mock_generate_menus.return_value = (mock_menu, None, menu_details)

        # Mock repository error
        mock_create_menu.return_value = (None, "Error saving menu", 500)

        response = self.client.get("/api/menu/1")
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Error saving menu")


if __name__ == "__main__":
    unittest.main()
