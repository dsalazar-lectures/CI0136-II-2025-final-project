import unittest
import datetime
import csv
from src.Database.User.PasswordResetTokenCSV import PasswordResetTokenCSV


class TestPasswordResetTokenCSV(unittest.TestCase):
    def get_valid_token(self, token: str):
        # Use UTC naive datetime so comparisons match test expectations.
        now = datetime.datetime.utcnow()

        with open(self.file_path, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["token"] == token and row["used"] == "False":
                    expires_at = datetime.datetime.fromisoformat(row["expires_at"])

                    # If expires_at came with a timezone (rare), drop it to naive
                    if expires_at.tzinfo is not None:
                        expires_at = expires_at.replace(tzinfo=None)

                    if expires_at > now:
                        return type(
                            "TokenData",
                            (),
                            {
                                "user_id": row["user_id"],
                                "expires_at": expires_at,
                            },
                        )

        return None

    def test_invalidate_token(self):
        import os
        from tempfile import NamedTemporaryFile

        with NamedTemporaryFile(delete=False) as tmp:
            path = tmp.name

        repo = PasswordResetTokenCSV(path)
        expires = datetime.datetime.now() + datetime.timedelta(hours=1)

        repo.create_token("1", "tok1", expires)
        repo.invalidate_token("tok1")

        token = repo.get_valid_token("tok1")
        self.assertIsNone(token)

        os.remove(path)
