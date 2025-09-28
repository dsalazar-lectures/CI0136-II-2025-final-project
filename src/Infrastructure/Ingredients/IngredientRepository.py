from typing import Dict, List, Optional

from ...Model.Ingredients.Ingredients import Ingredient

class IngredientRepository:

    def __init__(self) -> None:
        self._items: Dict[int, Ingredient] = {}
        self._next_id: int = 1
        self._seed() # mock data

    def get_all(self) -> List[Ingredient]:
        # return by alphabetical order
        return sorted(self._items.values(), key=lambda x: x.name.lower())