import unittest
from unittest.mock import patch
from flask import Flask
from src.Application.Menu import MenuUseCase
from src.API.Menu.menuRoutes import menu_bp
from src.Model.Menu.Menu import Menu
from src.Model.Menu.MenuDay import MenuDay


class MenuEndpointTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(menu_bp, url_prefix="/api")
        self.client = app.test_client()

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


if __name__ == "__main__":
    unittest.main()
