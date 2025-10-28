from typing import Dict
from typing import Callable
import streamlit as st
from datetime import datetime
from datetime import timedelta
import pandas as pd
from src.Application.Recipes.IRecipeRepository import IRecipeRepository
from src.Infrastructure.Recipes.CSVRecipeRepository import CSVRecipeRepository

# --------------------------------------------------------------------------------

MSG_NO_DATA_OR_FUNC = "No data or metrics available to display."
MSG_EXEC_ERROR_TPL = "Error executing the metric: {}"


# --------------------------------------------------------------------------------
class AnalysisLogs:
    @staticmethod
    def top_users_least_active():
        pass

    @staticmethod
    def top_users_most_active():
        pass

    @staticmethod
    def top_most_search_recipes(
        df_list, start_date, end_date, recipe_repo: IRecipeRepository | None = None
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
                
    def top_least_search_recipes(df_list, start_date, end_date, recipe_repo: IRecipeRepository | None = None):
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
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                week_ago = datetime.today() - timedelta(days=7)
                df = df[
                    (df["timestamp"] >= week_ago)
                    & (df["timestamp"] <= datetime.today())
                ]
                counts = df["Id_Producto"].value_counts(ascending=True)
                # st.write(f"all counts {counts}")
                counts = counts[counts < 5]
                # st.write(f"filtered counts {counts}")
                recipes_counts = {}
                for recipe_id in counts.index:
                    recipe = recipe_repo.get_by_id(recipe_id)
                    if recipe:
                        recipes_counts[recipe.to_dict()["name"]] = counts[recipe_id]

                st.bar_chart(recipes_counts)

    analysis_registry: Dict[str, Callable[..., None]] = {
        "Least Active Users": top_users_least_active,
        "Most Active Users": top_users_most_active,
        "Most Searched Recipes": top_most_search_recipes,
        "Least Searched Recipes": top_least_search_recipes,
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
