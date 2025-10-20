import logging
from typing import List, Optional
from pathlib import Path

class CustomLogger:

    def __init__(
        self,
        name: str = "AppLogger",
        handlers: Optional[List[logging.Handler]] = None,
        level: int = logging.DEBUG,
        add_console: bool = True,
        console_level: int = logging.DEBUG,
        log_dir: str = "src/database/Logs/",
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self._log_dir: Path = Path(log_dir)

        if handlers is None:
            formatter = self._build_default_formatter()
            handlers = self._build_default_handlers()

            for h in handlers:
                if h.formatter is None:
                    h.setFormatter(formatter)

            if add_console:
                console = logging.StreamHandler()
                console.setLevel(console_level)
                console.setFormatter(formatter)
                handlers.append(console)

        if not self.logger.handlers:
            for handler in handlers:
                self.logger.addHandler(handler)

    def _build_default_formatter(self) -> logging.Formatter:
        return logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | User: %(user)s | Role: %(role)s | Action: %(action)s | ID Object: %(id_object)s | Description: %(description)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    def _build_default_handlers(self) -> List[logging.Handler]:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        return [console]

    def log(self, level: str, user: str, role: str, action: str, id_object: int, description: str):
        extra = {"user": user, "role": role, "action": action, "id_object": id_object, "description": description}
        method = {
            "info": self.logger.info,
            "warning": self.logger.warning,
            "error": self.logger.error,
            "debug": self.logger.debug,
        }.get(level.lower(), self.logger.info)
        method("", extra=extra)