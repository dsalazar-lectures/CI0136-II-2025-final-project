import re
import logging
import unittest
from pathlib import Path
from unittest.mock import patch
from src.Shared.Logs.Logger_textfile import TxtFileLogger


def make_file_handler(target: Path, level: int = logging.DEBUG) -> logging.Handler:
    fh = logging.FileHandler(target, mode="a", encoding="utf-8")
    fh.setLevel(level)
    return fh


class TxtFileLoggerTests(unittest.TestCase):

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
        handler = make_file_handler(self.log_path)

        with patch.object(TxtFileLogger, "_build_default_handlers", return_value=[handler]):
            logger = TxtFileLogger()

        logger.log(
            level="info",
            user="alice",
            role="Chef",
            action="Create recipe",
            id_object=101,
            description="Created successfully"
        )

        self._flush_and_close(logger)
        content = self.log_path.read_text(encoding="utf-8")

        self.assertIn("User: alice", content)
        self.assertIn("Role: Chef", content)
        self.assertIn("Action: Create recipe", content)
        self.assertIn("ID Object: 101", content)
        self.assertIn("Description: Created successfully", content)

    def test_append_multiple_entries(self):
        handler = make_file_handler(self.log_path)

        with patch.object(TxtFileLogger, "_build_default_handlers", return_value=[handler]):
            logger = TxtFileLogger()

        logger.log("info", "user1", "Role1", "Action1", 1, "desc1")
        logger.log("warning", "user2", "Role2", "Action2", 2, "desc2")

        self._flush_and_close(logger)
        lines = self.log_path.read_text(encoding="utf-8").strip().splitlines()

        self.assertGreaterEqual(len(lines), 2)
        self.assertIn("User: user1", lines[0])
        self.assertIn("User: user2", lines[1])

    def test_log_format_contains_all_fields(self):
        handler = make_file_handler(self.log_path)

        with patch.object(TxtFileLogger, "_build_default_handlers", return_value=[handler]):
            logger = TxtFileLogger()

        logger.log("error", "bob", "User", "Delete recipe", 999, "Cannot delete")

        self._flush_and_close(logger)
        line = self.log_path.read_text(encoding="utf-8").strip().splitlines()[-1]

        self.assertIn(" | ERROR | ", line)
        self.assertRegex(
            line,
            r"User:\s+bob\s+\|\s+Role:\s+User\s+\|\s+Action:\s+Delete recipe\s+\|\s+ID Object:\s+999\s+\|\s+Description:\s+Cannot delete"
        )


if __name__ == "__main__":
    unittest.main()
