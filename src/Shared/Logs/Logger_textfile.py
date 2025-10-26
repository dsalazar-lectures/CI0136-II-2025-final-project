from src.Shared.Logs.Logger_component import CustomLogger
import logging
from typing import List
from pathlib import Path

class TxtFileLogger(CustomLogger):
    def __init__(self):
        self._filename = "GeneralLogs.txt"
        super().__init__()

    def _build_default_formatter(self) -> logging.Formatter:
        return super()._build_default_formatter()

    def _build_default_handlers(self) -> List[logging.Handler]:
        file_path: Path = self._log_dir / self._filename
        fh = logging.FileHandler(file_path, mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        return [fh]