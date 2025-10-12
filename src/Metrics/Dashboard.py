import streamlit as st
from pathlib import Path
from DashboardGeneralLogs import show_general_logs_window
from DashboardAnalysisLogs import show_analysis_logs_window
from AnalysisLogs import analysis_registry

st.set_page_config(page_title="Logs Dashboard", page_icon="📊", layout="wide")

dashboard_folder = Path(__file__).parent
available_files = list(dashboard_folder.glob("*.json"))


if not available_files:
    st.warning("⚠️ No JSON files found in the folder.")
    st.stop()

# --- Tab selection (mode) ---
mode = st.sidebar.selectbox(
    "Select an option:",
    ["General Data", "Logs Analysis"]
)

# --- Show the corresponding window ---
if mode == "General Data":
    show_general_logs_window(available_files)
elif mode == "Logs Analysis":
    show_analysis_logs_window(available_files, analysis_registry)
