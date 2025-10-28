import unittest
import json
from pathlib import Path
from src.Shared.Logs.custom_logger import CustomLogger
from src.Shared.Logs.json_file_handler import JsonFileHandler


class JsonFileHandlerAdvancedTests(unittest.TestCase):

    def setUp(self):
        self.log_dir = Path("test_logs")
        if self.log_dir.exists():
            for f in self.log_dir.glob("*.json"):
                f.unlink()
        else:
            self.log_dir.mkdir(parents=True, exist_ok=True)

        handler = JsonFileHandler(str(self.log_dir))
        self.logger = CustomLogger("TestLogger", handlers=[handler])

    def tearDown(self):
        for handler in self.logger.logger.handlers:
            handler.close()
        self.logger.logger.handlers.clear()

        for f in self.log_dir.glob("*.json"):
            f.unlink()
        if self.log_dir.exists():
            self.log_dir.rmdir()

    def _flush_and_close(self, logger):
        for handler in logger.logger.handlers:
            handler.flush()
            handler.close()
        logger.logger.handlers.clear()

    def _read_log_file(self, action: str):
        log_file = self.log_dir / f"{action.lower()}.json"
        self.assertTrue(log_file.exists(), f"Expected log file {log_file} not found.")
        with log_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    def test_missing_optional_id_object_defaults_to_dash(self):
        self.logger.log(
            "info", "UserX", "admin", "delete", description="Intento sin id_object"
        )
        self._flush_and_close(self.logger)

        data = self._read_log_file("delete")
        self.assertEqual(data[0]["id_object"], "-")

    def test_log_contains_all_expected_fields(self):
        self.logger.log("info", "user1", "Role1", "Action1", 1, "desc1")

        self._flush_and_close(self.logger)

        data = self._read_log_file("Action1")
        entry = data[0]
        expected_fields = {
            "timestamp",
            "level",
            "user",
            "role",
            "action",
            "id_object",
            "description",
        }
        self.assertTrue(expected_fields.issubset(entry.keys()))

    def test_logger_creates_directory_if_missing(self):
        import shutil

        temp_dir = Path("temp_logs_dir")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        handler = JsonFileHandler(str(temp_dir))
        logger = CustomLogger("DirTestLogger", handlers=[handler])

        logger.log("info", "U", "R", "TestAction", "1", description="check dir")
        for h in logger.logger.handlers:
            h.flush()
            h.close()

        log_file = temp_dir / "testaction.json"
        self.assertTrue(log_file.exists())

        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()
