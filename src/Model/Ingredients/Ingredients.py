# Here goes the ingredient object
class Ingredient:
    def __init__(self, id, name, categories, substitutes, components, recipe_count):
        self.id = id
        self.name = name
        self.categories = categories
        self.substitutes = substitutes
        self.components = components
        self.recipe_count = recipe_count
        self.format()

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "categories": self.categories,
            "substitutes": self.substitutes,
            "components": self.components,
            "recipe_count": self.recipe_count,
        }

    def __str__(self):
        return self.name

    def format(self):
        """Replace all spaces with hyphens"""
        self.name = self.name.replace(" ", "-")
        for index in range(len(self.categories)):
            self.categories[index] = self.categories[index].replace(" ", "-")
        for index in range(len(self.substitutes)):
            self.substitutes[index] = self.substitutes[index].replace(" ", "-")
        for index in range(len(self.components)):
            self.components[index] = self.components[index].replace(" ", "-")

    def has_substitutes(self):
        return len(self.substitutes) > 0

    def is_base_ingredient(self):
        return len(self.components) == 0

    def add_recipe(self):
        self.recipe_count = self.recipe_count + 1

    def change_categories(self, categories):
        self.categories = categories

    def change_substitutes(self, substitutes):
        self.substitutes = substitutes

    def change_components(self, components):
        self.components = components
