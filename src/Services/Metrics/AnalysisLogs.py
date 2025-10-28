from typing import Dict
from typing import Callable
import streamlit as st

# --------------------------------------------------------------------------------

MSG_NO_DATA_OR_FUNC = "No data or metrics available to display."
MSG_EXEC_ERROR_TPL = "Error executing the metric: {}"


# --------------------------------------------------------------------------------
class AnalysisLogs:
    @staticmethod
    def top_users_least_active():

        pass

    @staticmethod
    def top_users_most_active():
        pass

    analysis_registry: Dict[str, Callable[..., None]] = {
        "Least Active Users": top_users_least_active,
        "Most Active Users": top_users_most_active,
    }

    @staticmethod
    def show_analysis_logs(df_list, func):
        if df_list and func:
            try:
                func(df_list)
            except Exception as e:
                st.warning(MSG_EXEC_ERROR_TPL.format(e))
        else:
            st.info(MSG_NO_DATA_OR_FUNC)
