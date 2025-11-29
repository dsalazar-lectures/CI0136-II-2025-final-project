import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import unittest
from unittest.mock import patch, MagicMock
from src.Services.Metrics.AnalysisLogs import AnalysisLogs
from src.Shared.Logs.log_action_names import LogActionNames


class MostSearchRecipesPlotTest(unittest.TestCase):

    @patch("src.Services.Metrics.AnalysisLogs.st.text", new_callable=MagicMock)
    def test_top_most_search_recipes_with_no_data(self, mock_st_text):
        fake_df_list = []
        AnalysisLogs.top_most_search_recipes(fake_df_list)
        mock_st_text.assert_called_once_with("No data or metrics available to display.")

    @patch("src.Services.Metrics.AnalysisLogs.st.text", new_callable=MagicMock)
    def test_top_most_search_recipes_with_empty_data(self, mock_st_text):
        fake_df_list = [{"name": "Search recipes", "data": MagicMock(empty=True)}]
        AnalysisLogs.top_most_search_recipes(fake_df_list)
        mock_st_text.assert_called_once_with(
            f"No {LogActionNames.SEARCH_RECIPE.value.lower()} data found."
        )


if __name__ == "__main__":
    unittest.main()
