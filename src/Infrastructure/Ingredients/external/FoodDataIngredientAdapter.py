from typing import Optional, List, Dict
from src.Application.Interfaces.IExternalIngredientProvider import (
    IExternalIngredientProvider,
)
from src.Model.Ingredients.BaseIngredient import BaseIngredient
from src.Model.Ingredients.Ingredients import Ingredient
from .FoodDataAPIService import FoodDataAPIService


temp_id_counter = 20000


class FoodDataIngredientAdapter(IExternalIngredientProvider):
    """
    Adapter to integrate USDA FoodData Central API with our IngredientUseCase.
    """

    def __init__(self, api_service: FoodDataAPIService):
        self._api_service = api_service

    def search_ingredient(self, name: str) -> Optional[Ingredient]:
        """
        Interface to search for an ingredient by name using USDA FoodData Central API
        """
        global temp_id_counter

        fooddata_data = self._api_service.fetch_ingredient_data(name)

        if not fooddata_data:
            return None

        ingredient_name = fooddata_data.get("description", name).title()

        categories = self._map_categories(fooddata_data)

        substitutes = []

        temp_id = temp_id_counter
        temp_id_counter += 1

        return BaseIngredient(
            id=temp_id,
            name=ingredient_name,
            categories=categories,
            substitutes=substitutes,
            recipe_count=0,
        )

    def _map_categories(self, data: Dict) -> List[str]:
        categories = []

        # FoodData Central includes 'foodCategory' field
        food_category = data.get("foodCategory")
        if food_category:
            categories.append(food_category.replace(" ", "-").lower())

        return list(set(categories))
