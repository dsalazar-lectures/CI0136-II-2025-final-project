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
