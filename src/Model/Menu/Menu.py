from typing import List


class Menu:
    def __init__(self, menu_id: int):
        self.menu_id = menu_id  # TODO: assign based on csv file
        self.recipes = List[int]  # List of recipe IDs

    def to_dict(self):
        return {
            "menu_id": self.menu_id,
            "recipes": self.recipes,
        }
