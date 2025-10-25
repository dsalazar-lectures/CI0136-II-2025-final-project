import unittest, sys
from unittest.mock import patch
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3] / "src"))
from src.Services.Metrics.Dashboard import LogsDashboard

class TestLogsDashboard(unittest.TestCase):
    @patch("Services.Metrics.Dashboard.st.stop")
    @patch("Services.Metrics.Dashboard.st.warning")
    @patch("Services.Metrics.Dashboard.Path.glob")
    @patch("Services.Metrics.Dashboard.Path.exists")
    def test_get_available_json_file(self, mock_exists, mock_glob, mock_warning, mock_stop):
        mock_exists.return_value = True
        mock_glob.return_value = [Path("file1.json"), Path("file2.json")]
        dashboard = LogsDashboard(Path("/mock/dir"))

        files = dashboard.get_available_json_files()

        self.assertEqual(len(files), 2)
        mock_warning.assert_not_called()
        mock_stop.assert_not_called()

    @patch("Services.Metrics.Dashboard.st.stop")
    @patch("Services.Metrics.Dashboard.st.warning")
    @patch("Services.Metrics.Dashboard.Path.glob")
    @patch("Services.Metrics.Dashboard.Path.exists")
    def test_get_available_json_not_files(self, mock_exists, mock_glob, mock_warning, mock_stop):
        mock_exists.return_value = False
        mock_glob.return_value = []
        dashboard = LogsDashboard(Path("/mock/dir"))

        dashboard.get_available_json_files()

        mock_warning.assert_called_once()
        mock_stop.assert_called_once()

    @patch("Services.Metrics.Dashboard.st.sidebar.selectbox")
    def test_select_mode_Analysis(self, mock_selectbox):
        mock_selectbox.return_value = "Logs Analysis"
        dashboard = LogsDashboard(Path("/mock/dir"))

        mode = dashboard.select_mode()

        self.assertEqual(mode, "Logs Analysis")
        mock_selectbox.assert_called_once()

    @patch("Services.Metrics.Dashboard.st.sidebar.selectbox")
    def test_select_mode_General(self, mock_selectbox):
        mock_selectbox.return_value = "General Data"
        dashboard = LogsDashboard(Path("/mock/dir"))

        mode = dashboard.select_mode()

        self.assertEqual(mode, "General Data")
        mock_selectbox.assert_called_once()

    @patch("Services.Metrics.DashboardGeneralLogs.GeneralData_Window.show_general_logs_window")
    @patch("Services.Metrics.DashboardAnalysisLogs.Analysis_Window.show_analysis_logs_window")
    def test_render_mode_calls_correct_handler(self, mock_analysis, mock_general):
        dashboard = LogsDashboard()
        files = [Path("file1.json")]

        dashboard.render_mode(dashboard.MODE_GENERAL, files)
        mock_general.assert_called_once_with(files)

        dashboard.render_mode(dashboard.MODE_ANALYSIS, files)
        mock_analysis.assert_called_once()

    @patch("Services.Metrics.Dashboard.st.subheader")
    @patch("Services.Metrics.Dashboard.st.info")
    def test_render_mode_invalid_mode(self, mock_info, mock_subheader):
        dashboard = LogsDashboard()
        dashboard.render_mode("Unknown Mode", [])

        mock_subheader.assert_called_once()
        mock_info.assert_called_once()


# Run test: python -m unittest tests.Mocks.Dashboard.Mock_Dasboard -v