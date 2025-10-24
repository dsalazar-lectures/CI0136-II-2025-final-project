import unittest
from unittest.mock import patch, MagicMock
from src.Metrics.AnalysisLogs import AnalysisLogs


class LeastSearchRecipesPlotTest(unittest.TestCase):

    @patch("src.Metrics.AnalysisLogs.st.text", new_callable=MagicMock)
    def test_top_least_search_recipes_with_no_data(self, mock_st_text):
        fake_df_list = []
        AnalysisLogs.top_least_search_recipes(fake_df_list, None, None)
        mock_st_text.assert_called_once_with("No data or metrics available to display.")

    @patch("src.Metrics.AnalysisLogs.st.text", new_callable=MagicMock)
    def test_top_least_search_recipes_with_empty_data(self, mock_st_text):
        fake_df_list = [{"name": "Search recipes", "data": MagicMock(empty=True)}]
        AnalysisLogs.top_least_search_recipes(fake_df_list, None, None)
        mock_st_text.assert_called_once_with("No 'Search recipes' data found.")


if __name__ == "__main__":
    unittest.main()
