from typing import Dict, List, Optional
from Model.Ingredients.Ingredients import Ingredient

class IngredientRepository:
    def __init__(self) -> None:
        self._items: Dict[int, Ingredient] = {}
        self._next_id: int = 1
        self._seed()  # mock data

    def get_all(self) -> List[Ingredient]:
        # return by alphabetical order
        return sorted(self._items.values(), key=lambda x: x.name.lower())

    def get_by_id(self, ingredient_id: int) -> Optional[Ingredient]:
        return self._items.get(ingredient_id)

    def get_by_name(self, ingredient_name: str) -> Optional[Ingredient]:
        for ingredient in self._items.values():
            if ingredient.name.lower() == ingredient_name.lower():
                return ingredient
        return None
    
    def get_by_category(self, ingredient_category: str) -> List[Ingredient]:
        matching_ingredients = []
        for ingredient in self._items.values():
            if ingredient_category.lower() in [cat.lower() for cat in ingredient.categories]:
                matching_ingredients.append(ingredient)
        return matching_ingredients

    # part of the mocking
    def _add(
        self,
        name,
        *,
        categories=None,
        substitutes=None,
        components=None,
        recipe_count=0,
    ) -> None:
        iid = self._next_id
        self._next_id += 1
        self._items[iid] = Ingredient(
            id=iid,
            name=name,
            categories=list(categories or []),
            substitutes=list(substitutes or []),
            components=list(components or []),
            recipe_count=int(recipe_count),
        )

    def _seed(self) -> None:
        self._add(
            "Butter",
            categories=["dairy", "fat"],
            components=["lactose", "milk_protein"],
            recipe_count=42,
        )
        self._add(
            "Margarine",
            categories=["fat"],
            components=["soy", "plant_oils"],
            recipe_count=11,
        )
        self._add(
            "Whole Milk",
            categories=["dairy"],
            components=["lactose", "milk_protein"],
            recipe_count=55,
        )
        self._add(
            "Almond Milk",
            categories=["plant_milk"],
            components=["almond"],
            recipe_count=13,
        )
        self._add(
            "Wheat Flour",
            categories=["grain"],
            components=["gluten"],
            recipe_count=60,
        )
        self._add(
            "White Sugar",
            categories=["sweetener"],
            components=[],
            recipe_count=75,
        )
        self._add(
            "Egg",
            categories=["protein"],
            components=["egg_protein"],
            recipe_count=50,
        )
