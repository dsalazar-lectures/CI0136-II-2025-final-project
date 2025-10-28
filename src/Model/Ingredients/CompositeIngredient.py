from typing import List, Dict
from .Ingredients import Ingredient


class CompositeIngredient(Ingredient):
    def __init__(
        self,
        id,
        name,
        categories,
        substitutes,
        components,
        recipe_count,
    ) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.categories = list(categories or [])
        self.substitutes = list(substitutes or [])
        self.components = list(components or [])
        self.recipe_count = recipe_count

    def update_components(self, components: List[Ingredient]) -> None:
        self.components = list(components or [])

    def is_base_ingredient(self) -> bool:
        return False

    def to_json(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": "composite",
            "categories": list(self.categories),
            "substitutes": list(self.substitutes),
            "components": [str(comp) for comp in self.components],
            "recipe_count": self.recipe_count,
        }
