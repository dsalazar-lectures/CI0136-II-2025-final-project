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

        # Assert
        self.assertEqual(result["favorite_foods"], "")
        self.assertEqual(result["unfavorite_foods"], "")
        self.assertEqual(result["favorite_menus"], "")

        # Verify file content
        with open(self.temp_file.name, "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 2)  # Header + 1 data row
            data_line = lines[1].strip()
            self.assertEqual(data_line, "1,,,")
