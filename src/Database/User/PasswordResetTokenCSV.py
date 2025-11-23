import csv
import os
import datetime


class PasswordResetTokenCSV:
    def __init__(self, file_path="password_reset_tokens.csv"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["token", "user_id", "expires_at", "used"])

    def create_token(self, user_id: str, token: str, expires_at: datetime.datetime):
        with open(self.file_path, "a", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=["token", "user_id", "expires_at", "used"]
            )
            writer.writerow(
                {
                    "token": token,
                    "user_id": user_id,
                    "expires_at": expires_at.isoformat(),
                    "used": "False",
                }
            )

    def get_valid_token(self, token: str):
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["token"] == token and row["used"] == "False":
                    expires_at = datetime.datetime.fromisoformat(row["expires_at"])
                    return type(
                        "TokenData",
                        (),
                        {
                            "user_id": row["user_id"],
                            "expires_at": expires_at,
                        },
                    )
        return None

    def invalidate_token(self, token: str):
        rows = []
        updated = False

        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["token"] == token:
                    row["used"] = "True"
                    updated = True
                rows.append(row)

        if updated:
            with open(self.file_path, "w", newline="") as file:
                writer = csv.DictWriter(
                    file, fieldnames=["token", "user_id", "expires_at", "used"]
                )
                writer.writeheader()
                writer.writerows(rows)

    def invalidate_all_user_tokens(self, user_id: str):
        rows = []
        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["user_id"] == user_id and row["used"] == "False":
                    row["used"] = "True"
                rows.append(row)

        with open(self.file_path, "w", newline="") as file:
            writer = csv.DictWriter(
                file, fieldnames=["token", "user_id", "expires_at", "used"]
            )
            writer.writeheader()
            writer.writerows(rows)