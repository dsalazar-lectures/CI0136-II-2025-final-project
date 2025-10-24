class MockRecipe:
    def __init__(self, id, name, categories, ingredients=None, author=None):
        self.id = id
        self.name = name
        self.categories = categories
        self.ingredients = ingredients or []
        self.author = author

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "categories": self.categories,
            "ingredients": self.ingredients,
            "author": self.author,
        }


class MockRecipeRepo:
    """Simple dummy repository exposing find_by_category used by tests."""

    def __init__(self, recipes=None):
        self._recipes = recipes or []

    def find_by_category(self, category):
        return [r for r in self._recipes if category in r.categories]
