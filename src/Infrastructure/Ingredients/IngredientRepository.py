from typing import List, Optional
from src.Model.Ingredients.Ingredients import Ingredient
from src.Model.Ingredients.BaseIngredient import BaseIngredient
from src.Model.Ingredients.CompositeIngredient import CompositeIngredient


class IngredientRepository:
    def __init__(self):
        self._items: dict[int, Ingredient] = {}
        self._next_id: int = 1
        self._seed()  # mock data

    def get_all(self) -> List[Ingredient]:
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
            if ingredient_category.lower() in [
                cat.lower() for cat in ingredient.categories
            ]:
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
        ing_id = self._next_id
        self._next_id += 1
        if components is None or components == []:
            self._items[ing_id] = BaseIngredient(
                id=ing_id,
                name=name,
                categories=list(categories or []),
                substitutes=list(substitutes or []),
                recipe_count=int(recipe_count),
            )
        else:
            self._items[ing_id] = CompositeIngredient(
                id=ing_id,
                name=name,
                categories=list(categories or []),
                substitutes=list(substitutes or []),
                components=list(components or []),
                recipe_count=int(recipe_count),
            )

    def create_ingredient(
        self, name, categories, substitutes, components, recipe_count=0
    ):
        self._add(
            name,
            categories=categories,
            substitutes=substitutes,
            components=components,
            recipe_count=recipe_count,
        )

    def add_recipe(self, id: int):
        ingredient = self._items.get(id)
        if ingredient is None:
            return "ID is not valid"
        ingredient.add_recipe()

    def update_ingredient_categories(self, id: int, categories: List[str]):
        ingredient = self._items.get(id)
        if ingredient is None:
            return "ID is not valid"
        ingredient.update_categories(categories)

    def update_ingredient_substitutes(self, id: int, substitutes: List[str]):
        ingredient = self._items.get(id)
        if ingredient is None:
            return "ID is not valid"
        ingredient.update_substitutes(substitutes)

    def update_ingredient_components(self, id: int, components: List[str]):
        ingredient = self._items.get(id)
        if ingredient is None:
            return "ID is not valid"
        if ingredient.is_base_ingredient():
            return "Error: base ingredient"
        ingredient.update_commponents(components)

    def delete_ingredient(self, id: int):
        ingredient = self._items.pop(id, None)
        if ingredient is None:
            return "ID is not valid"

    def _seed(self) -> None:
        self._add(
            "Butter",
            categories=["lactose", "milk_protein", "fat"],
            substitutes=["Margarine"],
            recipe_count=42,
        )
        self._add(
            "Margarine",
            categories=["soy", "plant_oils", "fat"],
            recipe_count=11,
        )
        self._add(
            "Whole Milk",
            categories=["lactose", "milk_protein"],
            substitutes=["Almond Milk"],
            recipe_count=55,
        )
        self._add(
            "Almond Milk",
            categories=["plant_milk", "almond"],
            recipe_count=13,
        )
        self._add(
            "Wheat Flour",
            categories=["grain", "gluten"],
            recipe_count=60,
        )
        self._add(
            "White Sugar",
            categories=["sweetener"],
            recipe_count=75,
        )
        self._add(
            "Egg",
            categories=["protein", "egg_protein"],
            recipe_count=50,
        )
        self._add(
            "Strawberry",
            categories=["fruit"],
            recipe_count=5,
        )
        self._add(
            "Strawberry Jam",
            categories=["sweet"],
            components=["Strawberry", "White Sugar"],
            recipe_count=13,
        )
