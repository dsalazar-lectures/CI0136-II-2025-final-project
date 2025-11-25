from typing import Optional
from src.Application.Interfaces.IExternalIngredientProvider import (
    IExternalIngredientProvider,
)
from src.Model.Ingredients.BaseIngredient import BaseIngredient
from src.Model.Ingredients.Ingredients import Ingredient
from .SpoonacularAPIService import SpoonacularAPIService  # Importamos el servicio
from typing import List, Dict


temp_id_counter = 10000


class SpoonacularIngredientAdapter(IExternalIngredientProvider):
    """
    Adapter to integrate Spoonacular API with our IngredientUseCase.
    """

    def __init__(self, api_service: SpoonacularAPIService):
        self._api_service = api_service

    def search_ingredient(self, name: str) -> Optional[Ingredient]:
        """
        Interfase to search for an ingredient by name using Spoonacular API
        """
        global temp_id_counter

        spoonacular_data = self._api_service.fetch_ingredient_data(name)

        if not spoonacular_data:
            return None

        ingredient_name = spoonacular_data.get("name", name).title()

        categories = self._map_categories(spoonacular_data)

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

        aisle = data.get("aisle")
        if aisle:

            categories.append(aisle.replace(" ", "-").lower())

        return list(set(categories))
