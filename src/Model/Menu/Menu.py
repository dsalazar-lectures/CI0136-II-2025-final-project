class Menu:
    def __init__(
        self,
        menu_id: int,
        breakfast_id: int,
        lunch_id: int,
        dinner_id: int,
        dessert_id: int,
    ):
        self.menu_id = menu_id  # TODO: assign based on csv file
        self.breakfast = breakfast_id
        self.lunch = lunch_id
        self.dinner = dinner_id
        self.dessert = dessert_id

    def to_dict(self):
        return {
            "menu_id": self.menu_id,
            "breakfast": self.breakfast,
            "lunch": self.lunch,
            "dinner": self.dinner,
            "dessert": self.dessert,
        }
