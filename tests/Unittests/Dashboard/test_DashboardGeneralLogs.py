import json
import logging
import unittest
import sys
import tempfile
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3] / "src"))
sys.path.append(str(Path(__file__).resolve().parents[2] / "Mocks"))
from src.Services.Metrics.DashboardGeneralLogs import GeneralData_Window
from tests.Mocks.Dashboard.Mock_DashboardGeneralLogs import MocksDashboardGeneralLogs

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

    def test_show_general_logs_window_valid(self):
        prev = logging.root.manager.disable
        logging.disable(logging.WARNING)  
        try:
            patch_sidebar, patch_load, patch_kpis, patch_charts, patch_table = (
                MocksDashboardGeneralLogs.patch_show_general_logs_window_valid()
            )
            with patch_sidebar, patch_load, patch_kpis as mock_kpis, patch_charts as mock_charts, patch_table as mock_table:
                GeneralData_Window.show_general_logs_window([Path("mock.json")])
                mock_kpis.assert_called_once()
                mock_charts.assert_called_once()
                mock_table.assert_called_once()
        finally:
            logging.disable(prev)

    def test_show_general_logs_window_empty(self):
        prev = logging.root.manager.disable
        logging.disable(logging.WARNING)
        try:
            patch_sidebar, patch_warn, patch_stop = MocksDashboardGeneralLogs.patch_show_general_logs_window_empty()
            with patch_sidebar, patch_warn as mock_warn, patch_stop as mock_stop:
                GeneralData_Window.show_general_logs_window([])
                mock_warn.assert_called_once()
                mock_stop.assert_called()
        finally:
            logging.disable(prev)


    def test_sidebar_select_files_valid(self):
        with MocksDashboardGeneralLogs.patch_sidebar_select_files_valid() as mock_multiselect:
            result = GeneralData_Window.sidebar_select_files([Path("file1.json"), Path("file2.json")])
            self.assertEqual(len(result), 1)
            mock_multiselect.assert_called_once()

    def test_sidebar_select_files_empty(self):
        patch_multiselect, patch_info, patch_stop = MocksDashboardGeneralLogs.patch_sidebar_select_files_empty()

        with patch_multiselect, patch_info as mock_info, patch_stop as mock_stop:
            GeneralData_Window.sidebar_select_files([Path("file1.json")])
            mock_info.assert_called_once()
            mock_stop.assert_called_once()
