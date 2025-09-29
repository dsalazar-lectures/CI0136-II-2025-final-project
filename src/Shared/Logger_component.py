import logging
from typing import List, Optional


class CustomLogger:
    def __init__(self, name: str = "AppLogger", handlers: Optional[List[logging.Handler]] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        if handlers is None:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)

            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)s | Usuario: %(usuario)s | Rol: %(rol)s | Acción: %(accion)s | Descripción: %(descripcion)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            console_handler.setFormatter(formatter)
            handlers = [console_handler]

        if not self.logger.handlers:
            for handler in handlers:
                self.logger.addHandler(handler)