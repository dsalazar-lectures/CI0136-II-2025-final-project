import unittest
from unittest.mock import patch
from pathlib import Path

class MocksLogsDashboard(unittest.TestCase):
    @staticmethod
    def patch_get_available_json_file():
        return (
            patch("Services.Metrics.Dashboard.Path.exists", return_value=True),
            patch("Services.Metrics.Dashboard.Path.glob", return_value=[Path("file1.json"), Path("file2.json")]),
            patch("Services.Metrics.Dashboard.st.warning"),
            patch("Services.Metrics.Dashboard.st.stop")
        )

    @staticmethod
    def patch_get_available_json_not_files():
        return (
            patch("Services.Metrics.Dashboard.Path.exists", return_value=False),
            patch("Services.Metrics.Dashboard.Path.glob", return_value=[]),
            patch("Services.Metrics.Dashboard.st.warning"),
            patch("Services.Metrics.Dashboard.st.stop")
        )

    @staticmethod
    def patch_sidebar_selectbox(mode: str):
        return patch("Services.Metrics.Dashboard.st.sidebar.selectbox", return_value=mode)

    @staticmethod
    def patch_render_mode_handlers():
        return (
            patch("Services.Metrics.DashboardGeneralLogs.GeneralData_Window.show_general_logs_window"),
            patch("Services.Metrics.DashboardAnalysisLogs.Analysis_Window.show_analysis_logs_window")
        )

    @staticmethod
    def patch_render_mode_invalid():
        return (
            patch("Services.Metrics.Dashboard.st.subheader"),
            patch("Services.Metrics.Dashboard.st.info")
        )
