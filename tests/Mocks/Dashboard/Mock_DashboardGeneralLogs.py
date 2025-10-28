from unittest.mock import patch
from pathlib import Path
import pandas as pd
from src.Services.Metrics.DashboardGeneralLogs import GeneralData_Window


class MocksDashboardGeneralLogs:
    @staticmethod
    def patch_show_general_logs_window_valid():
        fake_df = pd.DataFrame(
            {
                "timestamp": ["2025-10-23"],
                "user": ["test"],
                "level": ["INFO"],
                "message": ["mock"],
            }
        )

        return (
            patch.object(
                GeneralData_Window,
                "sidebar_select_files",
                return_value=[Path("mock.json")],
            ),
            patch.object(
                GeneralData_Window, "load_logs_from_json", return_value=fake_df
            ),
            patch("src.Services.Metrics.DashboardGeneralLogs.GeneralLogs.show_kpis"),
            patch(
                "src.Services.Metrics.DashboardGeneralLogs.GeneralLogs.show_general_charts"
            ),
            patch(
                "src.Services.Metrics.DashboardGeneralLogs.GeneralLogs.show_logs_table"
            ),
        )

    @staticmethod
    def patch_show_general_logs_window_empty():
        return (
            patch.object(GeneralData_Window, "sidebar_select_files", return_value=[]),
            patch("src.Services.Metrics.DashboardGeneralLogs.st.warning"),
            patch("src.Services.Metrics.DashboardGeneralLogs.st.stop"),
            patch(
                "src.Services.Metrics.DashboardGeneralLogs.GeneralData_Window.sidebar_filters",
                return_value=(None, None, [], []),
            ),
            patch(
                "src.Services.Metrics.DashboardGeneralLogs.GeneralData_Window.apply_filters",
                return_value=pd.DataFrame(),  # evita KeyError en DataFrames vacíos
            ),
        )

    @staticmethod
    def patch_sidebar_select_files_valid():
        return patch(
            "src.Services.Metrics.DashboardGeneralLogs.st.sidebar.multiselect",
            return_value=[Path("file1.json")],
        )

    @staticmethod
    def patch_sidebar_select_files_empty():
        return (
            patch(
                "src.Services.Metrics.DashboardGeneralLogs.st.sidebar.multiselect",
                return_value=[],
            ),
            patch("src.Services.Metrics.DashboardGeneralLogs.st.info"),
            patch("src.Services.Metrics.DashboardGeneralLogs.st.stop"),
        )
