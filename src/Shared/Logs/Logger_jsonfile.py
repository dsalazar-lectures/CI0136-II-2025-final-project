import logging
from pathlib import Path
from typing import List
from src.Shared.Logs.Logger_component import CustomLogger
from src.Shared.Logs.json_formatter import JsonLineFormatter
from src.Shared.Logs.json_array_handler import JsonArrayHandler


class JsonFileLogger(CustomLogger):

    def __init__(self):
        self._filename = "ImportantLogs.json"
        super().__init__()

    def importantLog(
        self,
        level: str,
        user: str,
        role: str,
        action: str,
        description: str,
        id_object=None,
        msg: str = "",
    ):
        extra = {
            "user": user,
            "role": role,
            "action": action,
            "description": description,
            "id_object": id_object if id_object is not None else "-",
        }
        method = {
            "info": self.logger.info,
            "warning": self.logger.warning,
            "error": self.logger.error,
            "debug": self.logger.debug,
        }.get(level.lower(), self.logger.info)
        method(msg, extra=extra)

    def _build_default_formatter(self) -> logging.Formatter:
        return JsonLineFormatter()

    def _build_default_handlers(self) -> List[logging.Handler]:
        self._log_dir.mkdir(parents=True, exist_ok=True)
        path: Path = self._log_dir / self._filename
        h = JsonArrayHandler(path, level=logging.INFO)
        h.setFormatter(self._build_default_formatter())
        return [h]
