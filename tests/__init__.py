# Needed to make this directory a package
# and to run the tests in this directory
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]  # Subir desde /Tests
SRC_DIR = ROOT_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))