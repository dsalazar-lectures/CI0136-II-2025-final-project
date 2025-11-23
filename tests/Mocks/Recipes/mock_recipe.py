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
