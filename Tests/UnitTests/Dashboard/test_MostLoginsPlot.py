import unittest
from unittest.mock import patch
import pandas as pd

from src.Metrics.AnalysisLogs import AnalysisLogs

class MostLoginsPlotTest(unittest.TestCase):

    @patch("src.Metrics.AnalysisLogs.st")
    def test_no_data_shows_info(self, mock_st):
        AnalysisLogs.top_users_most_active(
            df_list=[], 
            start_date=pd.Timestamp("2025-10-10"),
            end_date=pd.Timestamp("2025-10-20"),
            top_n=10
        )
        mock_st.info.assert_called_once()
        mock_st.bar_chart.assert_not_called()

    @patch("src.Metrics.AnalysisLogs.st")
    def test_missing_columns_shows_info(self, mock_st):
        # Missing 'action'
        bad = pd.DataFrame({"timestamp": ["2025-10-12"], "user": ["Alice"]})
        AnalysisLogs.top_users_most_active(
            df_list=[{"name": "Login.json", "data": bad}],
            start_date=pd.Timestamp("2025-10-10"),
            end_date=pd.Timestamp("2025-10-20"),
            top_n=10
        )
        mock_st.info.assert_called()      # warns that columns are missing
        mock_st.bar_chart.assert_not_called()

    @patch("src.Metrics.AnalysisLogs.st")
    def test_counts_only_login_actions(self, mock_st):
        # Only these 3 count (action == "Login")
        df_login = pd.DataFrame({
            "timestamp": ["2025-10-12", "2025-10-13", "2025-10-13"],
            "user": ["Alice", "Bob", "Alice"],
            "action": ["Login", "Login", "Login"],
        })
        # These DO NOT count
        df_other = pd.DataFrame({
            "timestamp": ["2025-10-12", "2025-10-13"],
            "user": ["Alice", "Alice"],
            "action": ["Search recipe", "Delete recipe"],
        })

        AnalysisLogs.top_users_most_active(
            df_list=[{"name": "Login.json", "data": df_login},
                     {"name": "Share recipes.json", "data": df_other}],
            start_date=pd.Timestamp("2025-10-10"),
            end_date=pd.Timestamp("2025-10-20"),
            top_n=10
        )

        mock_st.bar_chart.assert_called_once()
        # We check the Series that was graphed
        series_passed = mock_st.bar_chart.call_args[0][0]
        # Only logins: Alice=2, Bob=1
        assert series_passed.to_dict() == {"Alice": 2, "Bob": 1}
        mock_st.dataframe.assert_called_once()

    @patch("src.Metrics.AnalysisLogs.st")
    def test_date_range_is_applied(self, mock_st):
        df_login = pd.DataFrame({
            "timestamp": ["2025-10-09", "2025-10-21", "2025-10-15"],
            "user": ["Alice", "Bob", "Alice"],
            "action": ["Login", "Login", "Login"],
        })

        AnalysisLogs.top_users_most_active(
            df_list=[{"name": "Login.json", "data": df_login}],
            start_date=pd.Timestamp("2025-10-10"),
            end_date=pd.Timestamp("2025-10-20"),
            top_n=10
        )

        series_passed = mock_st.bar_chart.call_args[0][0]
        # Only 2025-10-15 falls within the range => Alice=1
        assert series_passed.to_dict() == {"Alice": 1}
