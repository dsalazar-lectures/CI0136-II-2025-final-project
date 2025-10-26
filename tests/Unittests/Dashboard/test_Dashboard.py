import unittest, sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3] / "src"))

from src.Services.Metrics.Dashboard import LogsDashboard
from tests.Mocks.Dashboard.Mock_Dasboard import MocksLogsDashboard


class TestLogsDashboard(unittest.TestCase):
    def test_get_available_json_file(self):
        patch_exists, patch_glob, patch_warning, patch_stop = MocksLogsDashboard.patch_get_available_json_file()
        with patch_exists, patch_glob, patch_warning as mock_warning, patch_stop as mock_stop:
            dashboard = LogsDashboard(Path("/mock/dir"))
            files = dashboard.get_available_json_files()
            self.assertEqual(len(files), 2)
            mock_warning.assert_not_called()
            mock_stop.assert_not_called()

    def test_get_available_json_not_files(self):
        patch_exists, patch_glob, patch_warning, patch_stop = MocksLogsDashboard.patch_get_available_json_not_files()
        with patch_exists, patch_glob, patch_warning as mock_warning, patch_stop as mock_stop:
            dashboard = LogsDashboard(Path("/mock/dir"))
            dashboard.get_available_json_files()
            mock_warning.assert_called_once()
            mock_stop.assert_called_once()

    def test_select_mode_Analysis(self):
        with MocksLogsDashboard.patch_sidebar_selectbox("Logs Analysis") as mock_selectbox:
            dashboard = LogsDashboard(Path("/mock/dir"))
            mode = dashboard.select_mode()
            self.assertEqual(mode, "Logs Analysis")
            mock_selectbox.assert_called_once()

    def test_select_mode_General(self):
        with MocksLogsDashboard.patch_sidebar_selectbox("General Data") as mock_selectbox:
            dashboard = LogsDashboard(Path("/mock/dir"))
            mode = dashboard.select_mode()
            self.assertEqual(mode, "General Data")
            mock_selectbox.assert_called_once()

    def test_render_mode_calls_correct_handler(self):
        patch_general, patch_analysis = MocksLogsDashboard.patch_render_mode_handlers()
        with patch_general as mock_general, patch_analysis as mock_analysis:
            dashboard = LogsDashboard()
            files = [Path("file1.json")]

            dashboard.render_mode(dashboard.MODE_GENERAL, files)
            mock_general.assert_called_once_with(files)

            dashboard.render_mode(dashboard.MODE_ANALYSIS, files)
            mock_analysis.assert_called_once()

    def test_render_mode_invalid_mode(self):
        patch_subheader, patch_info = MocksLogsDashboard.patch_render_mode_invalid()
        with patch_subheader as mock_subheader, patch_info as mock_info:
            dashboard = LogsDashboard()
            dashboard.render_mode("Unknown Mode", [])
            mock_subheader.assert_called_once()
            mock_info.assert_called_once()
