class MockProfileRepo:
    def __init__(self):
        self.profiles = {}  # Not the CSV

    def create_profile(self, user_id: int):
        """Helper method to create test profiles"""
        self.profiles[user_id] = {"favorite_menus": []}

    def add_favorite_menu(self, user_id: int, menu_id: str) -> bool:
        if user_id not in self.profiles:
            return False  # User doesn't exist

        self.profiles[user_id]["favorite_menus"].append(menu_id)
        return True

    def remove_favorite_menu(self, user_id: int, menu_id: str) -> bool:
        # Duplicate check,
        # the one in the use case also happens to check for the user
        if user_id not in self.profiles:
            return False  # User doesn't exist

        self.profiles[user_id]["favorite_menus"].remove(menu_id)
        return True

    def get_favorite_menus(self, user_id: int) -> list:
        return self.profiles.get(user_id, {}).get("favorite_menus", [])

    def is_menu_in_favorites(self, user_id: int, menu_id: str) -> bool:
        return menu_id in self.get_favorite_menus(user_id)
