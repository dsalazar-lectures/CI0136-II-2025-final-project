import streamlit as st
import pandas as pd
import json
from GeneralLogs import show_kpis, show_general_charts, show_logs_table

def load_logs_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

def show_general_logs_window(available_files):
    df_list = []
    for file in available_files:
        df = load_logs_from_json(file)
        if not df.empty:
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            df_list.append(df)
            
    if not df_list:
        st.warning("No valid logs to display.")
        st.stop()

    logs_df = pd.concat(df_list, ignore_index=True)

    st.subheader("📊 General Data")
    show_kpis(logs_df)
    show_general_charts(logs_df)
    show_logs_table(logs_df)
