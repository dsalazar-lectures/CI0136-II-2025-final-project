import json
import logging
from datetime import datetime


class JsonLineFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "user": getattr(record, "user", "-"),
            "role": getattr(record, "role", "-"),
            "action": getattr(record, "action", "-"),
            "id_object": getattr(record, "id_object", "-"),
            "description": getattr(record, "description", "-"),
        }
        return json.dumps(payload, ensure_ascii=False)
