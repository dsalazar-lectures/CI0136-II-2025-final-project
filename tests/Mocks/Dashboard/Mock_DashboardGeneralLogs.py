import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3] / "src"))

from Metrics.DashboardGeneralLogs import GeneralData_Window
from Metrics.GeneralLogs import GeneralLogs

class TestDashboardGeneralLogs(unittest.TestCase):

    @patch.object(GeneralData_Window, "sidebar_select_files", return_value=[Path("mock.json")])
    @patch.object(GeneralData_Window, "load_logs_from_json")
    @patch.object(GeneralLogs, "show_kpis")
    @patch.object(GeneralLogs, "show_general_charts")
    @patch.object(GeneralLogs, "show_logs_table")
    def test_show_general_logs_window_valid(self, mock_table, mock_charts, mock_kpis, mock_load, mock_sidebar):
        df = pd.DataFrame({"timestamp": ["2025-10-23"], "user": ["test"], "level": ["INFO"]})
        mock_load.return_value = df

        GeneralData_Window.show_general_logs_window([Path("mock.json")])

        mock_kpis.assert_called_once()
        mock_charts.assert_called_once()
        mock_table.assert_called_once()

    @patch.object(GeneralData_Window, "sidebar_select_files", return_value=[])
    @patch("Metrics.DashboardGeneralLogs.st.warning")
    @patch("Metrics.DashboardGeneralLogs.st.stop")
    def test_show_general_logs_window_empty(self, mock_stop, mock_warn, mock_sidebar):
        GeneralData_Window.show_general_logs_window([])

        mock_warn.assert_called_once()
        mock_stop.assert_called_once()

    @patch("Metrics.DashboardGeneralLogs.st.sidebar.multiselect")
    def test_sidebar_select_files_valid(self, mock_multiselect):
        mock_multiselect.return_value = [Path("file1.json")]
        result = GeneralData_Window.sidebar_select_files([Path("file1.json"), Path("file2.json")])
        self.assertEqual(len(result), 1)

    @patch("Metrics.DashboardGeneralLogs.st.sidebar.multiselect", return_value=[])
    @patch("Metrics.DashboardGeneralLogs.st.info")
    @patch("Metrics.DashboardGeneralLogs.st.stop")
    def test_sidebar_select_files_empty(self, mock_stop, mock_info, mock_multiselect):
        GeneralData_Window.sidebar_select_files([Path("file1.json")])
        mock_info.assert_called_once()
        mock_stop.assert_called_once()

# Run test: python -m unittest tests.Mocks.Dashboard.Mock_GeneralLogs -v