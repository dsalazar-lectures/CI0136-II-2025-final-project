# Here goes the ingredient object
class Ingredient:
    def __init__(self, id, name, categories, substitutes,
                 components, recipe_count):
        self.id = id
        self.name = name
        self.categories = categories
        self.substitutes = substitutes
        self.components = components
        self.recipe_count = recipe_count

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'categories': self.categories,
            'substitutes': self.substitutes,
            'components': self.components,
            'recipe_count': self.recipe_count
        }

    def __str__(self):
        return self.name

    def has_substitutes(self):
        return len(self.substitutes) > 0

    def is_base_ingredient(self):
        return len(self.components) == 0
