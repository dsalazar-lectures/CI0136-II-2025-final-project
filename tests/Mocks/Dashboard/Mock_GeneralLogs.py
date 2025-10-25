import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[3] / "src"))

from Metrics.GeneralLogs import GeneralLogs

class TestGeneralLogs(unittest.TestCase):

    @patch("Metrics.GeneralLogs.st", new_callable=MagicMock)
    def test_show_logs_table_with_data(self, mock_st):
        df = pd.DataFrame({"user": ["u1"], "level": ["INFO"]})
        GeneralLogs.show_logs_table(df)
        mock_st.dataframe.assert_called_once_with(df)

    @patch("Metrics.GeneralLogs.st", new_callable=MagicMock)
    def test_show_logs_table_empty(self, mock_st):
        df = pd.DataFrame()
        GeneralLogs.show_logs_table(df)
        mock_st.info.assert_called_once()




# Run test: python -m unittest discover -s src/Test/Mocked -p "Mocks_GeneralLogs.py" -v