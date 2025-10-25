import json
from pathlib import Path
from typing import Iterable, Dict, Callable, List, Tuple
import pandas as pd
import streamlit as st

#------------------------------------------------------------------------------------
DATE_COL = "timestamp"
NAME_KEY = "name"
DATA_KEY = "data"

SUBHEADER_RESULTS = "📊 Analysis Results: {analysis}"

MSG_NO_VALID_JSON = "No valid JSON files could be loaded."
MSG_EXEC_ERROR_TPL = "Error executing the metric: {}"
#------------------------------------------------------------------------------------
class Analysis_Window:
    @staticmethod
    def load_logs_from_json(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return pd.DataFrame(data)
        except (OSError, json.JSONDecodeError, ValueError):
            return pd.DataFrame()

    @staticmethod
    def show_analysis_logs_window( available_files: Iterable[Path], analysis_registry: Dict[str, Callable[..., None]], ) -> None:
        logs_dataframes = Analysis_Window.build_named_frames(available_files)
        if not logs_dataframes:
            st.warning(MSG_NO_VALID_JSON)
            st.stop()

        start_date, end_date = Analysis_Window.combined_date_range(logs_dataframes)

        for name, func in analysis_registry.items():
            st.subheader(SUBHEADER_RESULTS.format(analysis=name))
            try:
                func(logs_dataframes, start_date, end_date)
            except Exception as e:
                st.warning(MSG_EXEC_ERROR_TPL.format(e))
            st.markdown("---")  

    @staticmethod
    def build_named_frames(available_files: Iterable[Path]) -> List[Dict[str, pd.DataFrame]]:
        out: List[Dict[str, pd.DataFrame]] = []
        for f in available_files:
            df = Analysis_Window.load_logs_from_json(f)
            if not df.empty:
                if DATE_COL in df.columns:
                    df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
                out.append({NAME_KEY: f.stem, DATA_KEY: df})
        return out
    
    @staticmethod
    def combined_date_range(items: List[Dict[str, pd.DataFrame]]) -> Tuple[pd.Timestamp, pd.Timestamp]:
        combined = pd.concat([d[DATA_KEY] for d in items], ignore_index=True)
        start = pd.to_datetime(combined[DATE_COL].min())
        end = pd.to_datetime(combined[DATE_COL].max())
        return start, end