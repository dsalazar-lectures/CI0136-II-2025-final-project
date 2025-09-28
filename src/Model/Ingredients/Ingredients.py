#Here goes the ingredient object
class Ingredient:
    def __init__(self, id, name, categories, substitutes, components, recipe_count):
        self.id = id
        self.name = name
        self.categories = categories
        self.substitutes = substitutes
        self.components = components
        self.recipe_count = recipe_count