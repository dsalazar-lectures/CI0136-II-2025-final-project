import json
from pathlib import Path
from typing import Iterable, List
import pandas as pd
import streamlit as st

from Services.Metrics.GeneralLogs import GeneralLogs


# ------------------------------------------------------------------------------------
DATE_COL = "timestamp"
USER_COL = "user"
LEVEL_COL = "level"

LABEL_SELECT_ACTION = "📂 Select Action"
LABEL_FILTERS = "Filters"
LABEL_START = "📅 Start Date"
LABEL_END = "📅 End Date"
LABEL_USER = "👤 User"
LABEL_LEVEL = "⚙️ Level"
LEVEL_GENERAL_DATA = "📊 General Data"

MSG_PICK = "Select at least one action to display logs."
MSG_EMPTY_SELECTION = "The selected files are empty or not valid."
# ------------------------------------------------------------------------------------


class GeneralData_Window:
    @staticmethod
    def load_logs_from_json(file_path: Path) -> pd.DataFrame:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return pd.DataFrame(data)
        except (OSError, json.JSONDecodeError, ValueError):
            return pd.DataFrame()

    @staticmethod
    def show_general_logs_window(available_files: Iterable[Path]) -> None:
        selected_files = GeneralData_Window.sidebar_select_files(available_files)
        df_list: list[pd.DataFrame] = []

        for file in selected_files:
            df = GeneralData_Window.load_logs_from_json(file)
            if not df.empty:
                df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
                df_list.append(df)

        if not df_list:
            st.warning(MSG_EMPTY_SELECTION)
            st.stop()

        logs_df = GeneralData_Window.concat_non_empty(df_list)
        start_date, end_date, selected_levels, selected_users = (
            GeneralData_Window.sidebar_filters(logs_df)
        )
        filtered_df = GeneralData_Window.apply_filters(
            logs_df, start_date, end_date, selected_levels, selected_users
        )

        st.subheader(LEVEL_GENERAL_DATA)
        if not filtered_df.empty:
            GeneralLogs.show_kpis(filtered_df)
            GeneralLogs.show_general_charts(filtered_df)
            GeneralLogs.show_logs_table(filtered_df)
        else:
            st.info("No data to display.")

    @staticmethod
    def sidebar_select_files(available_files: Iterable[Path]) -> list[Path]:
        selected = st.sidebar.multiselect(
            LABEL_SELECT_ACTION,
            options=list(available_files),
            format_func=lambda x: x.stem,
        )
        if not selected:
            st.info(MSG_PICK)
            st.stop()
        return selected

    @staticmethod
    def sidebar_filters(df: pd.DataFrame):
        st.sidebar.header(LABEL_FILTERS)

        start_date = st.sidebar.date_input(LABEL_START, df[DATE_COL].min())
        end_date = st.sidebar.date_input(LABEL_END, df[DATE_COL].max())

        levels = sorted(df[LEVEL_COL].dropna().unique())
        selected_levels = st.sidebar.multiselect(LABEL_LEVEL, levels, default=levels)

        users = sorted(df[USER_COL].dropna().unique())
        selected_users = st.sidebar.multiselect(LABEL_USER, users, default=users)

        return start_date, end_date, selected_levels, selected_users

    @staticmethod
    def apply_filters(
        df: pd.DataFrame,
        start_date,
        end_date,
        selected_levels: List[str],
        selected_users: List[str],
    ) -> pd.DataFrame:
        out = df.copy()
        if selected_levels:
            out = out[out[LEVEL_COL].isin(selected_levels)]
        if selected_users:
            out = out[out[USER_COL].isin(selected_users)]

        out = out[
            out[DATE_COL].between(pd.to_datetime(start_date), pd.to_datetime(end_date))
        ]
        return out

    @staticmethod
    def concat_non_empty(dfs: List[pd.DataFrame]) -> pd.DataFrame:
        valid = [d for d in dfs if not d.empty]
        return pd.concat(valid, ignore_index=True) if valid else pd.DataFrame()
