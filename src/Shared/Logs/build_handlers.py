from pathlib import Path
import logging
from src.Shared.Logs.text_file_handler import TxtFileHandler
from src.Shared.Logs.json_file_handler import JsonFileHandler


def build_handlers(out_dir: str = "src/database/Logs"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | User:%(user)s | Role:%(role)s | Action:%(action)s | ID:%(id_object)s | %(description)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    txt_handler = TxtFileHandler(str(Path(out_dir) / "GeneralLogs.txt"))
    json_handler = JsonFileHandler(str(Path(out_dir)))

    return [console, txt_handler, json_handler]
