import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3] / "src"))

import json
import unittest
import pandas as pd
import tempfile
from src.Services.Metrics.DashboardGeneralLogs import GeneralData_Window

class TestDashboardGeneralLogs(unittest.TestCase):

    def test_load_logs_from_json_valid(self):
        data = [{"user": "test", "level": "INFO"}]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            json.dump(data, tmp)
            tmp_path = Path(tmp.name)

        df = GeneralData_Window.load_logs_from_json(tmp_path)
        self.assertFalse(df.empty)
        self.assertIn("user", df.columns)

    def test_load_logs_from_json_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp:
            tmp.write("{invalid json}")
            tmp_path = Path(tmp.name)

        df = GeneralData_Window.load_logs_from_json(tmp_path)
        self.assertTrue(df.empty)




# Run test: ython -m unittest tests.Unittests.Dashboard.test_DashboardGeneralLogs -v