import unittest
import csv
import os
import tempfile
from src.Database.Profiles.ProfileCSV import ProfileCSV


class TestProfileCSV(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix="_test_profiles.csv"
        )
        self.temp_file.close()

        with open(self.temp_file.name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["user_id", "favorite_foods", "unfavorite_foods", "favorite_menus"]
            )

        self.profile_csv = ProfileCSV(self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_create_profile_success(self):
        # Arrange
        profile_data = {
            "user_id": 1,
            "favorite_foods": [],
            "unfavorite_foods": [],
            "favorite_menus": [],
        }

        # Act
        result = self.profile_csv.create_profile(profile_data)

        # Assert - create_profile returns CSV format (strings)
        self.assertEqual(result["favorite_foods"], "")
        self.assertEqual(result["unfavorite_foods"], "")
        self.assertEqual(result["favorite_menus"], "")

        # Verify file content
        with open(self.temp_file.name, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)  # Header + 1 data row
            data_line = lines[1].strip()
            self.assertEqual(data_line, "1,,,")

    def test_get_profile_returns_lists(self):
        """Test that get_profile returns lists, not strings"""
        # Arrange
        profile_data = {
            "user_id": 1,
            "favorite_foods": ["apple", "banana"],
            "unfavorite_foods": ["onion"],
            "favorite_menus": ["menu1"],
        }
        self.profile_csv.create_profile(profile_data)

        # Act
        result = self.profile_csv.get_profile(1)

        # Assert - get_profile should return lists
        self.assertIsNotNone(result)
        self.assertEqual(result["user_id"], 1)
        self.assertIsInstance(result["favorite_foods"], list)
        self.assertEqual(result["favorite_foods"], ["apple", "banana"])
        self.assertIsInstance(result["unfavorite_foods"], list)
        self.assertEqual(result["unfavorite_foods"], ["onion"])
        self.assertIsInstance(result["favorite_menus"], list)
        self.assertEqual(result["favorite_menus"], ["menu1"])

    def test_get_profile_empty_lists(self):
        """Test that get_profile returns empty lists for empty fields"""
        # Arrange
        profile_data = {
            "user_id": 2,
            "favorite_foods": [],
            "unfavorite_foods": [],
            "favorite_menus": [],
        }
        self.profile_csv.create_profile(profile_data)

        # Act
        result = self.profile_csv.get_profile(2)

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result["favorite_foods"], [])
        self.assertEqual(result["unfavorite_foods"], [])
        self.assertEqual(result["favorite_menus"], [])
