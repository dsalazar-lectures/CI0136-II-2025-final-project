import json
import logging
from pathlib import Path


class JsonFileHandler(logging.Handler):
    def __init__(self, path: str, level: int = logging.INFO):
        super().__init__(level)
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.formatter = logging.Formatter(datefmt="%Y-%m-%d %H:%M:%S")

    def emit(self, record: logging.LogRecord) -> None:
        try:
            timestamp = self.formatter.formatTime(record, self.formatter.datefmt)

            log_entry = {
                "timestamp": timestamp,
                "level": record.levelname,
                "user": getattr(record, "user", "-"),
                "role": getattr(record, "role", "-"),
                "action": getattr(record, "action", "-"),
                "id_object": getattr(record, "id_object", "-"),
                "description": getattr(record, "description", "-"),
            }

            data = []
            if self.path.exists():
                try:
                    content = self.path.read_text(encoding="utf-8").strip()
                    if content:
                        data = json.loads(content)
                        if not isinstance(data, list):
                            data = []
                except json.JSONDecodeError:
                    data = []

            data.append(log_entry)
            self.path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
            )

        except Exception:
            self.handleError(record)
