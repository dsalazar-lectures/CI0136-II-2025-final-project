import unittest
import datetime
from src.Database.User.PasswordResetTokenCSV import PasswordResetTokenCSV


class TestPasswordResetTokenCSV(unittest.TestCase):
    def test_create_and_get_token(self):
        import os
        from tempfile import NamedTemporaryFile

        with NamedTemporaryFile(delete=False) as tmp:
            path = tmp.name

        repo = PasswordResetTokenCSV(path)
        expires = datetime.datetime.now() + datetime.timedelta(hours=1)

        repo.create_token("10", "abc123", expires)

        token = repo.get_valid_token("abc123")

        self.assertIsNotNone(token)
        self.assertEqual(token.user_id, "10")

        os.remove(path)

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
