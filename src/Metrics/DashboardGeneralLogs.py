import json
from pathlib import Path
from typing import Iterable, List
import pandas as pd
import streamlit as st

from Metrics.GeneralLogs import GeneralLogs


#------------------------------------------------------------------------------------
DATE_COL = "timestamp"
USER_COL = "user"
LEVEL_COL = "level"

LABEL_SELECT_ACTION = "📂 Select Action"
LEVEL_GENERAL_DATA = "📊 General Data"

MSG_PICK = "Select at least one action to display logs."
MSG_EMPTY_SELECTION = "The selected files are empty or not valid."
#------------------------------------------------------------------------------------
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

        st.subheader(LEVEL_GENERAL_DATA)
        if not logs_df.empty:
            GeneralLogs.show_kpis(logs_df)
            GeneralLogs.show_general_charts(logs_df)
            GeneralLogs.show_logs_table(logs_df)
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
    def concat_non_empty(dfs: List[pd.DataFrame]) -> pd.DataFrame:
        valid = [d for d in dfs if not d.empty]
        return pd.concat(valid, ignore_index=True) if valid else pd.DataFrame()