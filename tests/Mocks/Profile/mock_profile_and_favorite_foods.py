from src.Application.Profiles.IProfileRepository import IProfileRepository
from src.Model.Profiles.Profiles import Profile


class MockProfileAndFavoriteFoods(IProfileRepository):
    """Mock implementation of IProfileRepository for testing"""

    def __init__(self):
        self.profiles = {}

    def create_profile(self, user_id) -> Profile:
        if user_id in self.profiles:
            return None
        profile = Profile(
            user_id=user_id, favorite_foods=[], unfavorite_foods=[], favorite_menus=[]
        )
        self.profiles[user_id] = profile
        return profile

    def get_profile(self, user_id) -> Profile:
        return self.profiles.get(user_id)

    def update_favorite_foods(self, user_id, favorites) -> Profile:
        if user_id not in self.profiles:
            return None
        profile = self.profiles[user_id]
        profile.favorite_foods = favorites
        return profile

    # Favorite Menu helpers
    def add_favorite_menu(self, user_id: int, menu_id: str) -> bool:
        profile = self.profiles.get(user_id)
        if not profile:
            return False
        if menu_id in profile.favorite_menus:
            return False
        profile.favorite_menus.append(menu_id)
        return True

    def remove_favorite_menu(self, user_id: int, menu_id: str) -> bool:
        profile = self.profiles.get(user_id)
        if not profile:
            return False
        if menu_id not in profile.favorite_menus:
            return False
        profile.favorite_menus.remove(menu_id)
        return True

    def get_favorite_menus(self, user_id: int) -> list:
        profile = self.profiles.get(user_id)
        if not profile:
            return []
        return list(profile.favorite_menus)

    def is_menu_in_favorites(self, user_id: int, menu_id: str) -> bool:
        profile = self.profiles.get(user_id)
        if not profile:
            return False
        return menu_id in profile.favorite_menus

    def delete_profile(self, user_id: int) -> bool:
        if user_id in self.profiles:
            del self.profiles[user_id]
            return True
        return False
