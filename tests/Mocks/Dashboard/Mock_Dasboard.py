import unittest
from unittest.mock import patch
from pathlib import Path


class MocksLogsDashboard(unittest.TestCase):
    @staticmethod
    def patch_get_available_json_file():
        return (
            patch("src.Services.Metrics.Dashboard.Path.exists", return_value=True),
            patch(
                "src.Services.Metrics.Dashboard.Path.glob",
                return_value=[Path("file1.json"), Path("file2.json")],
            ),
            patch("src.Services.Metrics.Dashboard.st.warning"),
            patch("src.Services.Metrics.Dashboard.st.stop"),
        )

    @staticmethod
    def patch_get_available_json_not_files():
        return (
            patch("src.Services.Metrics.Dashboard.Path.exists", return_value=False),
            patch("src.Services.Metrics.Dashboard.Path.glob", return_value=[]),
            patch("src.Services.Metrics.Dashboard.st.warning"),
            patch("src.Services.Metrics.Dashboard.st.stop"),
        )

    @staticmethod
    def patch_sidebar_selectbox(mode: str):
        return patch(
            "src.Services.Metrics.Dashboard.st.sidebar.selectbox", return_value=mode
        )

    @staticmethod
    def patch_render_mode_handlers():
        return (
            patch(
                "src.Services.Metrics.DashboardGeneralLogs.GeneralData_Window.show_general_logs_window"
            ),
            patch(
                "src.Services.Metrics.DashboardAnalysisLogs.Analysis_Window.show_analysis_logs_window"
            ),
        )

    @staticmethod
    def patch_render_mode_invalid():
        return (
            patch("src.Services.Metrics.Dashboard.st.subheader"),
            patch("src.Services.Metrics.Dashboard.st.info"),
        )
