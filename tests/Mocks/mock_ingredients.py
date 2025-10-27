# tests/Mocks/ingredients_mocks.py


class MockIngredient:
    def __init__(self, id, name, categories=None, components=None):
        self.id = id
        self.name = name
        self.categories = categories if categories is not None else ["Dairy"]
        self.components = components if components is not None else ["Milk", "Fat"]

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "categories": self.categories,
            "components": self.components,
        }


INGREDIENT_1 = MockIngredient(id=1, name="Butter", categories=["Fat"])
INGREDIENT_2 = MockIngredient(id=2, name="Milk", categories=["Dairy"])
INGREDIENT_3 = MockIngredient(id=3, name="Cheese", categories=["Dairy"])

SIMPLE_INGREDIENT_1 = {"id": 1, "name": "Butter"}
SIMPLE_INGREDIENT_2 = {"id": 2, "name": "Milk"}
SIMPLE_INGREDIENT_3 = {"id": 3, "name": "Cheese"}
