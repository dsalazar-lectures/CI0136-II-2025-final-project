import logging
from typing import List, Optional


class CustomLogger:
    def __init__(
        self, name: str = "AppLogger", handlers: Optional[List[logging.Handler]] = None
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if handlers is None:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)s | Usuario: %(usuario)s | Rol: %(rol)s | Acción: %(accion)s | Descripción: %(descripcion)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            console_handler.setFormatter(formatter)
            handlers = [console_handler]

        if not self.logger.handlers:
            for handler in handlers:
                self.logger.addHandler(handler)

    def log(self, level: str, usuario: str, rol: str, accion: str, descripcion: str):
        extra = {
            "usuario": usuario,
            "rol": rol,
            "accion": accion,
            "descripcion": descripcion,
        }

        log_method = {
            "info": self.logger.info,
            "warning": self.logger.warning,
            "error": self.logger.error,
            "debug": self.logger.debug,
        }.get(level.lower(), self.logger.info)

        log_method("", extra=extra)
