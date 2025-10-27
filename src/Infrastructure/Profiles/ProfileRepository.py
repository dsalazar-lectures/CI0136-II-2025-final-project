from src.Application.Profiles.IProfileRepository import IProfileRepository
from src.Model.Profiles.Profiles import Profile
from src.Database.Profiles.ProfileCSV import ProfileCSV


class ProfileRepository(IProfileRepository):
    def __init__(self, csv_file_path="profiles.csv"):
        self.profile_database = ProfileCSV(csv_file_path)

    def create_profile(self, user_id: int) -> Profile:
        profile_data = {
            "user_id": user_id,
            "favorite_foods": [],
            "unfavorite_foods": [],
            "favorite_menus": [],
        }
        created_profile_data = self.profile_database.create_profile(profile_data)
        if created_profile_data:
            return Profile(
                user_id=int(created_profile_data["user_id"]),
                favorite_foods=created_profile_data["favorite_foods"],
                unfavorite_foods=created_profile_data["unfavorite_foods"],
                favorite_menus=created_profile_data["favorite_menus"],
            )
        return None

    # Favorite Menu Functions
    def add_favorite_menu(self, user_id: str, menu_id: str) -> bool:
        """Add a menu to user's favorites"""
        profile_data = self.profile_database.get_profile_by_user_id(user_id)
        if not profile_data:
            return False

        favorite_menus = profile_data.get("favorite_menus", [])
        if menu_id in favorite_menus:
            return False  # Already exists

        favorite_menus.append(menu_id)
        profile_data["favorite_menus"] = favorite_menus

        return self.profile_database.update_profile(user_id, profile_data)

    def remove_favorite_menu(self, user_id: str, menu_id: str) -> bool:
        """Remove a menu from user's favorites"""
        profile_data = self.profile_database.get_profile_by_user_id(user_id)
        if not profile_data:
            return False

        favorite_menus = profile_data.get("favorite_menus", [])
        if menu_id not in favorite_menus:
            return False  # Not in favorites

        favorite_menus.remove(menu_id)
        profile_data["favorite_menus"] = favorite_menus

        return self.profile_database.update_profile(user_id, profile_data)

    def get_favorite_menus(self, user_id: str) -> list:
        """Get all favorite menu IDs for a user"""
        profile_data = self.profile_database.get_profile_by_user_id(user_id)
        if not profile_data:
            return []

        return profile_data.get("favorite_menus", [])

    def is_menu_in_favorites(self, user_id: str, menu_id: str) -> bool:
        """Check if a menu is in user's favorites"""
        favorite_menus = self.get_favorite_menus(user_id)
        return menu_id in favorite_menus
