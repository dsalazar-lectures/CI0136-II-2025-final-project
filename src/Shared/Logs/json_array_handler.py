import json
import logging
from pathlib import Path


class JsonArrayHandler(logging.Handler):

    def __init__(
        self,
        file_path: Path,
        level: int = logging.DEBUG,
        encoding: str = "utf-8",
        indent: int = 2,
    ):
        super().__init__(level=level)
        self.file_path = Path(file_path)
        self.encoding = encoding
        self.indent = indent

    def emit(self, record: logging.LogRecord) -> None:
        try:
            formatted = self.format(record)
            obj = json.loads(formatted) if isinstance(formatted, str) else formatted

            data = []
            if self.file_path.exists() and self.file_path.stat().st_size > 0:
                with self.file_path.open("r", encoding=self.encoding) as f:
                    try:
                        loaded = json.load(f)
                        if isinstance(loaded, list):
                            data = loaded
                    except json.JSONDecodeError:
                        data = []

            data.append(obj)

            with self.file_path.open("w", encoding=self.encoding) as f:
                json.dump(data, f, ensure_ascii=False, indent=self.indent)
        except Exception:
            self.handleError(record)
