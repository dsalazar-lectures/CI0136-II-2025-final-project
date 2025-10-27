import logging
import unittest
from pathlib import Path
from src.Shared.Logs.custom_logger import CustomLogger
from src.Shared.Logs.text_file_handler import TxtFileHandler


class TxtFileHandlerTests(unittest.TestCase):

    def setUp(self):
        self.log_path = Path("testLogs.txt")
        if self.log_path.exists():
            self.log_path.unlink()

    def tearDown(self):
        for handler in logging.getLogger().handlers[:]:
            handler.close()
            logging.getLogger().removeHandler(handler)

        if self.log_path.exists():
            self.log_path.unlink()

    def _flush_and_close(self, logger):
        for handler in logger.logger.handlers:
            handler.flush()
            handler.close()
        logger.logger.handlers.clear()

    def test_write_single_log_entry(self):
        handler = TxtFileHandler(str(self.log_path))
        logger = CustomLogger("TestLogger", handlers=[handler])

        logger.log(
            level="info",
            user="alice",
            role="Chef",
            action="Create recipe",
            id_object=101,
            description="Created successfully",
        )

        self._flush_and_close(logger)
        content = self.log_path.read_text(encoding="utf-8")

        self.assertIn("User:alice", content)
        self.assertIn("Role:Chef", content)
        self.assertIn("Action:Create recipe", content)
        self.assertIn("ID:101", content)
        self.assertIn("Created successfully", content)

    def test_append_multiple_entries(self):
        handler = TxtFileHandler(str(self.log_path))
        logger = CustomLogger("TestLogger", handlers=[handler])

        logger.log("info", "user1", "Role1", "Action1", 1, "desc1")
        logger.log("warning", "user2", "Role2", "Action2", 2, "desc2")

        self._flush_and_close(logger)
        lines = self.log_path.read_text(encoding="utf-8").strip().splitlines()

        self.assertGreaterEqual(len(lines), 2)
        self.assertIn("User:user1", lines[0])
        self.assertIn("User:user2", lines[1])

    def test_log_format_contains_all_fields(self):
        handler = TxtFileHandler(str(self.log_path))
        logger = CustomLogger("TestLogger", handlers=[handler])

        logger.log("error", "bob", "User", "Delete recipe", 999, "Cannot delete")

        self._flush_and_close(logger)
        line = self.log_path.read_text(encoding="utf-8").strip().splitlines()[-1]

        self.assertIn(" | ERROR | ", line)
        self.assertIn("User:bob", line)
        self.assertIn("Role:User", line)
        self.assertIn("Action:Delete recipe", line)
        self.assertIn("ID:999", line)
        self.assertIn("Cannot delete", line)


if __name__ == "__main__":
    unittest.main()
