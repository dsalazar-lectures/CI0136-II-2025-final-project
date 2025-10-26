from typing import List, Dict, Callable
import pandas as pd
import streamlit as st

# --------------------------------------------------------------------------------

MSG_NO_DATA_OR_FUNC = "No data or metrics available to display."
MSG_EXEC_ERROR_TPL = "Error executing the metric: {}"
DATE_COL = "timestamp"
USER_COL = "user"
ACTION_COL = "action"
ACTION_VALUE_LOGIN = "Login"


# --------------------------------------------------------------------------------
class AnalysisLogs:
    # Example metric functions
    @staticmethod
    def top_users_least_active(df_list, start_date, end_date):
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
    def top_users_most_active(df_list, start_date, end_date, top_n: int = 10):
        """Top N de usuarios con MÁS INICIOS DE SESIÓN (action == 'Login') en el rango dado."""
        df = AnalysisLogs._concat_and_filter(df_list, start_date, end_date)

        # Minimum validation
        if df.empty or not {"user", "action"}.issubset(df.columns):
            st.info(
                "No hay datos suficientes ('user' y 'action') para calcular logins."
            )
            return

        # Login events only (exact match)
        df = df[df[ACTION_COL] == ACTION_VALUE_LOGIN]
        if df.empty:
            st.info("No hay inicios de sesión en el rango seleccionado.")
            return

        counts = df[USER_COL].value_counts().head(top_n)
        st.write(
            f"Rango: **{start_date.date()} – {end_date.date()}** · Inicios de sesión: **{len(df)}**"
        )
        st.bar_chart(counts)
        st.dataframe(counts.rename_axis("user").reset_index(name="logins"))

    analysis_registry: Dict[str, Callable[..., None]] = {
        "Least Active Users": top_users_least_active,
        "Users with Most Logins": top_users_most_active,
    }

    @staticmethod
    def show_analysis_logs(df_list, func, start_date, end_date):
        if df_list and func:
            try:
                func(df_list, start_date, end_date)
            except Exception as e:
                st.warning(MSG_EXEC_ERROR_TPL.format(e))
        else:
            st.info(MSG_NO_DATA_OR_FUNC)
