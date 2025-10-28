from typing import Callable, Dict, List
import pandas as pd
import streamlit as st

# --------------------------------------------------------------------------------

MSG_NO_DATA_OR_FUNC = "No data or metrics available to display."
MSG_EXEC_ERROR_TPL = "Error executing the metric: {}"
DATE_COL = "timestamp"
USER_COL = "user"
ACTION_COL = "action"
LEVEL_COL = "level"
ERROR_LEVELS = {"ERROR"}  # Only errors only (no warnings)


# --------------------------------------------------------------------------------
class AnalysisLogs:
    @staticmethod
    def top_users_least_active():

        pass

    @staticmethod
    def _concat_and_filter(df_list, start_date, end_date) -> pd.DataFrame:
        frames: List[pd.DataFrame] = []
        for item in df_list:
            df = item.get("data")
            if not isinstance(df, pd.DataFrame):
                continue
            df = df.dropna(axis=1, how="all")
            if df.empty or df.dropna(how="all").empty:
                continue
            if DATE_COL in df.columns and not pd.api.types.is_datetime64_any_dtype(
                df[DATE_COL]
            ):
                df = df.copy()
                df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
            frames.append(df)

        if not frames:
            return pd.DataFrame()

        all_df = pd.concat(frames, ignore_index=True)

        if DATE_COL in all_df.columns:
            mask = (all_df[DATE_COL] >= start_date) & (all_df[DATE_COL] <= end_date)
            all_df = all_df.loc[mask]
        return all_df

    @staticmethod
    def top_error_categories(df_list, start_date, end_date, top_n: int = 5):
        """Top N action categories producing the most errors (level == 'ERROR')."""
        df = AnalysisLogs._concat_and_filter(df_list, start_date, end_date)

        if df.empty or not {ACTION_COL, LEVEL_COL}.issubset(df.columns):
            st.info("No error logs found (missing 'action' or 'level').")
            return

        err = df[df[LEVEL_COL].isin(ERROR_LEVELS)].copy()
        if err.empty:
            st.info("No ERROR entries in the selected range.")
            return

        # simple category mapping by action text
        def to_category(action: str) -> str:
            a = str(action).strip().lower()
            if "recipe" in a:  # Create/Get/Update/Delete/Search recipe
                return "Recipes"
            if a in {"login", "account lock"}:
                return "Authentication"
            return str(action).strip() or "Unknown"

        err["category"] = err[ACTION_COL].apply(to_category)
        counts = err["category"].value_counts().head(top_n)

        st.subheader("Analysis Results: Error Categories (Top 5)")
        st.write(
            f"Range: **{start_date.date()} – {end_date.date()}** · Errors: **{len(err)}**"
        )
        st.bar_chart(counts)
        st.dataframe(counts.rename_axis("category").reset_index(name="errors"))

    @staticmethod
    def top_users_most_active():
        pass

    analysis_registry: Dict[str, Callable[..., None]] = {
        "Least Active Users": top_users_least_active,
        "Error Categories (Top 5)": top_error_categories,
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
