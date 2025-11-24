from typing import Callable, Dict, List
import pandas as pd
import streamlit as st
from src.Application.Recipes.IRecipeRepository import IRecipeRepository
from src.Infrastructure.Recipes.CSVRecipeRepository import CSVRecipeRepository
from datetime import datetime, timedelta


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
    def top_most_search_recipes(
        df_list,
        recipe_repo: IRecipeRepository | None = None,
    ):
        recipe_repo = recipe_repo or CSVRecipeRepository()
        if df_list is None or len(df_list) == 0:
            st.text(MSG_NO_DATA_OR_FUNC)
        else:
            df = None
            for item in df_list:
                if item["name"] == "Search recipes":
                    df = item["data"]
                    break

            if df is None or df.empty:
                st.text("No 'Search recipes' data found.")
            else:
                counts = df["Id_Producto"].value_counts().head(10)
                recipes_counts = {}
                for recipe_id in df["Id_Producto"].unique():
                    recipe = recipe_repo.get_by_id(recipe_id)
                    if recipe:
                        recipes_counts[recipe.to_dict()["name"]] = counts[recipe_id]

                st.bar_chart(recipes_counts)

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

    analysis_registry: Dict[str, Callable[..., None]] = {
        "Error Categories (Top 5)": top_error_categories,
        "Most Searched Recipes": top_most_search_recipes,
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
