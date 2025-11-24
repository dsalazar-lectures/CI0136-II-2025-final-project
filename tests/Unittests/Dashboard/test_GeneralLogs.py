import unittest
from pathlib import Path
import sys

# for parent in Path(__file__).resolve().parents:
#     print(parent)
sys.path.append(str(Path(__file__).resolve().parents[3]))
sys.path.append(str(Path(__file__).resolve().parents[2] / "Mocks"))

from src.Services.Metrics.GeneralLogs import GeneralLogs
from tests.Mocks.Dashboard.Mock_GeneralLogs import MocksGeneralLogs


class TestGeneralLogs(unittest.TestCase):
    def test_show_logs_table_with_data(self):
        df = MocksGeneralLogs.get_sample_df()
        with MocksGeneralLogs.patch_st() as mock_st:
            GeneralLogs.show_logs_table(df)
            mock_st.dataframe.assert_called_once_with(df)

    def test_show_logs_table_empty(self):
        df = MocksGeneralLogs.get_empty_df()
        with MocksGeneralLogs.patch_st() as mock_st:
            GeneralLogs.show_logs_table(df)
            mock_st.info.assert_called_once()
