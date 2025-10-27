import logging
from pathlib import Path


class TxtFileHandler(logging.Handler):
    def __init__(self, path: str, level: int = logging.INFO):
        super().__init__(level)
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        fmt = "%(asctime)s | %(levelname)s | User:%(user)s | Role:%(role)s | Action:%(action)s | ID:%(id_object)s | %(description)s"
        self.setFormatter(logging.Formatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S"))

    def emit(self, record: logging.LogRecord) -> None:
        try:
            line = self.format(record)
            with self.path.open("a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            self.handleError(record)
