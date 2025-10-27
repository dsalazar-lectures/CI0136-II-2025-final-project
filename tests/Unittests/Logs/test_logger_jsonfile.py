import unittest
import json
from pathlib import Path
from src.Shared.Logs.custom_logger import CustomLogger
from src.Shared.Logs.json_file_handler import JsonFileHandler


class JsonFileHandlerAdvancedTests(unittest.TestCase):

    def setUp(self):
        self.log_path = Path("testLogs.json")
        if self.log_path.exists():
            self.log_path.unlink()

        handler = JsonFileHandler(str(self.log_path))
        self.logger = CustomLogger("TestLogger", handlers=[handler])

    def tearDown(self):
        for handler in self.logger.logger.handlers:
            handler.close()
        self.logger.logger.handlers.clear()

        if self.log_path.exists():
            self.log_path.unlink()

    def _flush_and_close(self, logger):
        for handler in logger.logger.handlers:
            handler.flush()
            handler.close()
        logger.logger.handlers.clear()

    def test_missing_optional_id_object_defaults_to_dash(self):
        self.logger.log(
            "info", "UserX", "admin", "delete", description="Intento sin id_object"
        )
        self._flush_and_close(self.logger)

        with self.log_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data[0]["id_object"], "-")

    def test_log_contains_all_expected_fields(self):
        self.logger.log("info", "user1", "Role1", "Action1", 1, "desc1")

        self._flush_and_close(self.logger)

        with self.log_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

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

        temp_dir.mkdir(parents=True, exist_ok=True)
        log_file = temp_dir / "log.json"

        handler = JsonFileHandler(str(log_file))
        logger = CustomLogger("DirTestLogger", handlers=[handler])

        logger.log("info", "U", "R", "A", "D", description="check dir")
        for h in logger.logger.handlers:
            h.flush()
            h.close()

        self.assertTrue(log_file.exists())
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    unittest.main()
