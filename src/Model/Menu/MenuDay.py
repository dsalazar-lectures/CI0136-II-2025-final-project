class MenuDay:
    def __init__(
        self,
        breakfast_recipe_id: int,
        lunch_recipe_id: int,
        dinner_recipe_id: int,
        dessert_recipe_id: int,
    ):
        self.breakfast = breakfast_recipe_id
        self.lunch = lunch_recipe_id
        self.dinner = dinner_recipe_id
        self.dessert = dessert_recipe_id

    def to_dict(self):
        return {
            "breakfast": self.breakfast,
            "lunch": self.lunch,
            "dinner": self.dinner,
            "dessert": self.dessert,
        }
