import csv
import os


class UserCSV:
    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['id', 'username', 'password', 'email', 'role'])

    def user_exists(self, username, email):
        with open(self.file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username or row['email'] == email:
                    return True
        return False

    def create_user(self, user_dto):

        next_id = 1
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', newline='') as file:
                reader = csv.DictReader(file)
                # Collects existing IDs
                ids = [int(row['id']) for row in reader if row['id'].isdigit()]
                if ids:
                    next_id = max(ids) + 1

        new_user = {
            'id': str(next_id),
            'username': user_dto.username,
            'password': user_dto.password,
            'email': user_dto.email,
            'role': user_dto.role
        }

        # Appends new user to CSV file
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.DictWriter(
                file, fieldnames=['id', 'username', 'password', 'email', 'role'])
            writer.writerow(new_user)

        return new_user
    
    def get_user_by_username(self, username):
        with open(self.file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    return row
        return None
