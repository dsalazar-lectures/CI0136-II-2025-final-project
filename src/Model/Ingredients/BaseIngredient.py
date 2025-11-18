from typing import Dict
from .Ingredients import Ingredient


class BaseIngredient(Ingredient):
    def __init__(self, id, name, categories, substitutes, recipe_count) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.categories = categories
        self.substitutes = substitutes
        self.recipe_count = recipe_count
        self._format_fields()

    def is_base_ingredient(self) -> bool:
        return True

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": "base",
            "categories": list(self.categories),
            "substitutes": list(self.substitutes),
            "recipe_count": self.recipe_count,
        }
