import logging
from dataclasses import asdict
from typing import Iterable, Optional
from src.Shared.Logs.audit_event import AuditEvent


class CustomLogger:

    def __init__(
        self,
        name: str = "AppLogger",
        handlers: Optional[Iterable[logging.Handler]] = None,
        level: int = logging.DEBUG,
    ) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        if handlers is not None and not self.logger.handlers:
            for h in handlers:
                self.logger.addHandler(h)

    def log(
        self,
        level: str,
        user: str,
        role: str,
        action: str,
        id_object: int | str = "-",
        description: str = "",
    ) -> None:
        event = AuditEvent(
            user=user,
            role=role,
            action=action,
            id_object=id_object,
            description=description,
        )
        extra = asdict(event)

        method = {
            "info": self.logger.info,
            "warning": self.logger.warning,
            "error": self.logger.error,
            "debug": self.logger.debug,
        }.get(level.lower(), self.logger.info)

        method("", extra=extra)
