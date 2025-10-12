import streamlit as st

def show_kpis(df):
    unique_users = df["user"].nunique() if "user" in df else 0
    total_logs = len(df)
    info_count = (df["level"] == "INFO").sum() if "level" in df else 0
    warning_count = (df["level"] == "WARNING").sum() if "level" in df else 0
    error_count = (df["level"] == "ERROR").sum() if "level" in df else 0

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Unique Users", unique_users)
    col2.metric("Total Logs", total_logs)
    col3.metric("INFO Logs", info_count)
    col4.metric("WARNING Logs", warning_count)
    col5.metric("ERROR Logs", error_count)

def show_general_charts(df):
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("Top Users by Activity")
        user_counts = df["user"].value_counts().head(10)
        st.bar_chart(user_counts)
    with col_g2:
        st.subheader("Distribution by Log Level")
        level_counts = df["level"].value_counts()
        st.bar_chart(level_counts)

def show_logs_table(df):
    st.markdown("### 📋 Logs Details")
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No logs loaded or filters returned no results.")
