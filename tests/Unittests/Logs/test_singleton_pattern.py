import unittest
from src.Shared.Logs.custom_logger import CustomLogger


class TestSingletonCustomLogger(unittest.TestCase):
    def test_same_instance(self):
        logger1 = CustomLogger()
        logger2 = CustomLogger()

        self.assertIs(logger1, logger2, "CustomLogger is not acting as a Singleton")

    def test_instance_persists_state(self):
        logger1 = CustomLogger()
        logger1.some_attribute = "persistent"

        logger2 = CustomLogger()
        self.assertEqual(
            logger2.some_attribute,
            "persistent",
            "The Singleton state is not preserved across instances",
        )

    def test_logger_has_single_instance_id(self):
        logger1 = CustomLogger()
        logger2 = CustomLogger()
        logger3 = CustomLogger()

        self.assertEqual(
            logger1._instance_id,
            logger2._instance_id,
            "Logger instances have different IDs (not Singleton)",
        )
        self.assertEqual(logger1._instance_id, logger3._instance_id)

    def test_new_with_different_args_returns_same_instance(self):
        logger1 = CustomLogger()
        logger2 = CustomLogger(handlers=[])

        self.assertIs(
            logger1,
            logger2,
            "CustomLogger created a new instance when different arguments were passed",
        )


if __name__ == "__main__":
    unittest.main()

