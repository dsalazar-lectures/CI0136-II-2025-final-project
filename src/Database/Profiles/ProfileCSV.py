import csv
import os


class ProfileCSV:
    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['user_id', 'favorite_foods', 'unfavorite_foods', 'favorite_menus'])

    def create_profile(self, profile_data):

        new_profile = {
            'user_id': str(profile_data['user_id']),
            'favorite_foods': ';'.join(profile_data['favorite_foods']),
            'unfavorite_foods': ';'.join(profile_data['unfavorite_foods']),
            'favorite_menus': ';'.join(profile_data['favorite_menus'])
        }

        # Appends new profile to CSV file
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=['user_id', 'favorite_foods', 'unfavorite_foods', 'favorite_menus'])
            writer.writerow(new_profile)

        return new_profile
