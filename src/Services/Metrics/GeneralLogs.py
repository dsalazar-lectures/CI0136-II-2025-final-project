import pandas as pd
import streamlit as st

USER_COL = "user"
LEVEL_COL = "level"
LEVEL_LOGS_DETAILS = "### 📋 Logs Details"


class GeneralLogs:
    @staticmethod
    def show_kpis(df: pd.DataFrame):
        unique_users = df[USER_COL].nunique() if USER_COL in df else 0
        total_logs = len(df)

        level_series = df[LEVEL_COL] if LEVEL_COL in df else pd.Series(dtype="object")
        info_count = (level_series == "INFO").sum()
        warning_count = (level_series == "WARNING").sum()
        error_count = (level_series == "ERROR").sum()

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Unique Users", unique_users)
        col2.metric("Total Logs", total_logs)
        col3.metric("INFO Logs", info_count)
        col4.metric("WARNING Logs", warning_count)
        col5.metric("ERROR Logs", error_count)

    @staticmethod
    def show_general_charts(df: pd.DataFrame):
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.subheader("Top Users by Activity")
            if USER_COL in df:
                user_counts = df[USER_COL].value_counts().head(10)
                st.bar_chart(user_counts)
            else:
                st.info("No 'user' column found.")

        with col_g2:
            st.subheader("Distribution by Log Level")
            if LEVEL_COL in df:
                level_counts = df[LEVEL_COL].value_counts()
                st.bar_chart(level_counts)
            else:
                st.info("No 'level' column found.")

    @staticmethod
    def show_logs_table(df: pd.DataFrame):
        st.markdown(LEVEL_LOGS_DETAILS)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No logs loaded or filters returned no results.")
