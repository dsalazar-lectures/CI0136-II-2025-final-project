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
                writer.writerow(["id", "username", "password", "email", "role", "key"])

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
            "id": str(next_id),
            "username": user_dto.username,
            "password": user_dto.password,
            "email": user_dto.email,
            "role": user_dto.role,
            "key": getattr(user_dto, "key", "") or "",
        }

        # Appends new user to CSV file
        with open(self.file_path, "a", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "id",
                    "username",
                    "password",
                    "email",
                    "role",
                    "key",
                ],
            )
            writer.writerow(new_user)

        return new_user

    def get_user_by_username(self, username):
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    return row
        return None

    def get_user_by_id(self, user_id):
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["id"] == str(user_id):
                    return row
        return None

    def get_user_by_token(self, token):
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["token"] == token:
                    return row

        return None

    def update_user_key(self, username, new_key):
        updated = False
        tmp = NamedTemporaryFile("w", delete=False, newline="")
        with open(self.file_path, "r", newline="") as src, tmp:
            reader = csv.DictReader(src)
            fieldnames = reader.fieldnames or [
                "id",
                "username",
                "password",
                "email",
                "role",
                "key",
            ]
            if "key" not in fieldnames:
                fieldnames.append("key")

            writer = csv.DictWriter(tmp, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                if row.get("username") == username:
                    row["key"] = new_key
                    updated = True
                for col in fieldnames:
                    row.setdefault(col, "")
                writer.writerow(row)

        shutil.move(tmp.name, self.file_path)
        return updated

    def update_password(self, username, hashed_password):
        updated = False
        rows = []
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    row["password"] = hashed_password
                    updated = True
                rows.append(row)

        if updated:
            with open(self.file_path, "w", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "id",
                        "username",
                        "password",
                        "email",
                        "role",
                        "key",
                        "token",
                    ],
                )
                writer.writeheader()
                writer.writerows(rows)
            return True, "Password updated successfully", 200

        return False, "Failed to update password", 400

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by user_id"""
        rows = []
        deleted = False

        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row["id"] == str(user_id):
                    deleted = True
                    continue  # Skip adding this row to the new list
                rows.append(row)

        if deleted:
            with open(self.file_path, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

        return deleted

    def update_email(self, username, new_email):
        updated = False
        rows = []

        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username:
                    row["email"] = new_email
                    updated = True
                rows.append(row)

        if updated:
            with open(self.file_path, "w", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["id", "username", "password", "email", "role", "key"],
                )
                writer.writeheader()
                writer.writerows(rows)
            return True, "Email updated successfully", 200

        return False, "User not found", 404