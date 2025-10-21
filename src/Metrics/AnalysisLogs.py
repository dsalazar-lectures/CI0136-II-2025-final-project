from typing import List, Dict, Any, Tuple, Optional
import pandas as pd
import streamlit as st

#--------------------------------------------------------------------------------

MSG_NO_DATA_OR_FUNC = "No data or metrics available to display."
MSG_EXEC_ERROR_TPL = "Error executing the metric: {}"

#--------------------------------------------------------------------------------

# Example metric functions
def top_users_least_active(df_list, start_date, end_date): 
    pass


def top_users_most_active(df_list, start_date, end_date):
    pass


analysis_registry = {
    "Least Active Users": top_users_least_active,
    "Most Active Users": top_users_most_active,
}

def show_analysis_logs(df_list, func, start_date, end_date):
    if df_list and func:
        try:
            func(df_list, start_date, end_date)
        except Exception as e:
            st.warning(MSG_EXEC_ERROR_TPL.format(e))
    else:
        st.info(MSG_NO_DATA_OR_FUNC)
