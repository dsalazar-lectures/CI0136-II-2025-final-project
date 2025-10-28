import json
import logging
from pathlib import Path


class JsonFileHandler(logging.Handler):
    def __init__(self, base_dir: str = "src/database/Logs", level: int = logging.INFO):
        super().__init__(level)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.formatter = logging.Formatter(datefmt="%Y-%m-%d %H:%M:%S")

    def _get_file_for_action(self, action: str) -> Path:
        safe_action = str(action).strip().replace(" ", "_").lower() or "general"
        return self.base_dir / f"{safe_action}.json"

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

            action = getattr(record, "action", "general")
            log_file = self._get_file_for_action(action)

            data = []
            if log_file.exists():
                try:
                    content = log_file.read_text(encoding="utf-8").strip()
                    if content:
                        data = json.loads(content)
                        if not isinstance(data, list):
                            data = []
                except json.JSONDecodeError:
                    data = []

            data.append(log_entry)
            log_file.write_text(
                json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
            )

        except Exception:
            self.handleError(record)
