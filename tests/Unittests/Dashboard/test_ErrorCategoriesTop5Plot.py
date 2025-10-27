import unittest
from unittest.mock import patch
import pandas as pd

from src.Metrics.AnalysisLogs import AnalysisLogs


class ErrorCategoriesPlotTest(unittest.TestCase):

    @patch("src.Metrics.AnalysisLogs.st")
    def test_no_data_shows_info(self, mock_st):
        AnalysisLogs.top_error_categories(
            df_list=[],
            start_date=pd.Timestamp("2025-10-10"),
            end_date=pd.Timestamp("2025-10-20"),
            top_n=5,
        )
        mock_st.info.assert_called_once()
        mock_st.bar_chart.assert_not_called()

    @patch("src.Metrics.AnalysisLogs.st")
    def test_missing_columns_shows_info(self, mock_st):
        # Missing 'level'
        bad = pd.DataFrame(
            {
                "timestamp": ["2025-10-12"],
                "action": ["Create recipe"],
            }
        )
        AnalysisLogs.top_error_categories(
            df_list=[{"name": "ImportantLogs.json", "data": bad}],
            start_date=pd.Timestamp("2025-10-10"),
            end_date=pd.Timestamp("2025-10-20"),
            top_n=5,
        )
        mock_st.info.assert_called()  # warns about missing columns
        mock_st.bar_chart.assert_not_called()

    @patch("src.Metrics.AnalysisLogs.st")
    def test_counts_only_error_level_and_category_mapping(self, mock_st):
        # Only ERROR rows should be counted; WARNING/INFO are ignored
        df = pd.DataFrame(
            {
                "timestamp": [
                    "2025-10-12",
                    "2025-10-12",
                    "2025-10-13",
                    "2025-10-13",
                    "2025-10-14",
                    "2025-10-14",
                ],
                "action": [
                    "Create recipe",  # Recipes (ERROR)
                    "Delete recipe",  # Recipes (ERROR)
                    "Login",  # Authentication (ERROR)
                    "Account lock",  # Authentication (ERROR)
                    "Update recipe",  # Recipes (INFO) -> ignored
                    "Search recipe",  # Recipes (WARNING) -> ignored
                ],
                "level": ["ERROR", "ERROR", "ERROR", "ERROR", "INFO", "WARNING"],
            }
        )

        AnalysisLogs.top_error_categories(
            df_list=[{"name": "ImportantLogs.json", "data": df}],
            start_date=pd.Timestamp("2025-10-10"),
            end_date=pd.Timestamp("2025-10-20"),
            top_n=5,
        )

        mock_st.bar_chart.assert_called_once()
        series_passed = mock_st.bar_chart.call_args[0][0]
        # Expected: Recipes=2, Authentication=2 (only ERRORs)
        assert series_passed.to_dict() == {"Recipes": 2, "Authentication": 2}
        mock_st.dataframe.assert_called_once()

    @patch("src.Metrics.AnalysisLogs.st")
    def test_date_range_is_applied(self, mock_st):
        df = pd.DataFrame(
            {
                "timestamp": ["2025-10-09", "2025-10-15"],
                "action": ["Create recipe", "Delete recipe"],
                "level": ["ERROR", "ERROR"],
            }
        )

        AnalysisLogs.top_error_categories(
            df_list=[{"name": "ImportantLogs.json", "data": df}],
            start_date=pd.Timestamp("2025-10-10"),
            end_date=pd.Timestamp("2025-10-20"),
            top_n=5,
        )

        series_passed = mock_st.bar_chart.call_args[0][0]
        # Only 2025-10-15 is in range => Recipes=1
        assert series_passed.to_dict() == {"Recipes": 1}


if __name__ == "__main__":
    unittest.main()
