import csv
import os
from tempfile import NamedTemporaryFile
import shutil

class UserCSV:
    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    ['id', 'username', 'password', 'email', 'role', 'key', 'token'])

    def user_exists(self, username, email):
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username or row["email"] == email:
                    return True
        return False

    def create_user(self, user_dto):

        next_id = 1
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", newline="") as file:
                reader = csv.DictReader(file)
                # Collects existing IDs
                ids = [int(row["id"]) for row in reader if row["id"].isdigit()]
                if ids:
                    next_id = max(ids) + 1

        new_user = {
            'id': str(next_id),
            'username': user_dto.username,
            'password': user_dto.password,
            'email': user_dto.email,
            'role': user_dto.role,
            'key': getattr(user_dto, 'key', '') or '',
            'token': ''
        }

        # Appends new user to CSV file
        with open(self.file_path, "a", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=['id', 'username', 'password', 'email', 'role', 'key', 'token'])
            writer.writerow(new_user)

        return new_user

    def get_user_by_username(self, username):
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    return row
        return None
    
    def update_user_token(self, username, token, key=None):
        updated = False
        tmp = NamedTemporaryFile('w', delete=False, newline='')
        with open(self.file_path, 'r', newline='') as src, tmp:
            reader = csv.DictReader(src)
            fieldnames = reader.fieldnames or ['id','username','password','email','role','key','token']
            for col in ['key', 'token']:
                if col not in fieldnames:
                    fieldnames.append(col)
            writer = csv.DictWriter(tmp, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                if row.get('username') == username:
                    row['token'] = token
                    if key is not None:
                        row['key'] = key
                    updated = True
                for col in fieldnames:
                    row.setdefault(col, '')
                writer.writerow(row)

        shutil.move(tmp.name, self.file_path)
        return updated
