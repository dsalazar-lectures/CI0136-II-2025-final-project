class Menu:
    def __init__(
        self,
        menu_id: int,
        breakfast_recipe_id: int,
        lunch_recipe_id: int,
        dinner_recipe_id: int,
        dessert_recipe_id: int,
    ):
        self.menu_id = menu_id  # TODO: assign based on csv file
        # TODO: Create MenuDailyRecipes class to encapsulate daily recipes
        self.breakfast = breakfast_recipe_id
        self.lunch = lunch_recipe_id
        self.dinner = dinner_recipe_id
        self.dessert = dessert_recipe_id

    def to_dict(self):
        return {
            "menu_id": self.menu_id,
            "breakfast": self.breakfast,
            "lunch": self.lunch,
            "dinner": self.dinner,
            "dessert": self.dessert,
        }
