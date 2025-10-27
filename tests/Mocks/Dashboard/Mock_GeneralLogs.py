from unittest.mock import patch, MagicMock
import pandas as pd


class MocksGeneralLogs:
    @staticmethod
    def patch_st():
        return patch("src.Services.Metrics.GeneralLogs.st", new_callable=MagicMock)

    @staticmethod
    def get_sample_df():
        return pd.DataFrame({"user": ["u1"], "level": ["INFO"]})

    @staticmethod
    def get_empty_df():
        return pd.DataFrame()
