from typing import Optional
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
                favorite_foods=(
                    created_profile_data["favorite_foods"].split(";")
                    if created_profile_data["favorite_foods"]
                    else []
                ),
                unfavorite_foods=(
                    created_profile_data["unfavorite_foods"].split(";")
                    if created_profile_data["unfavorite_foods"]
                    else []
                ),
                favorite_menus=(
                    created_profile_data["favorite_menus"].split(";")
                    if created_profile_data["favorite_menus"]
                    else []
                ),
            )
        return None

    def get_profile(self, user_id) -> Optional[Profile]:
        data = self.profile_database.get_profile(user_id)
        if not data:
            return None
        return Profile(
            user_id=int(data["user_id"]),
            favorite_foods=data["favorite_foods"],
            unfavorite_foods=data["unfavorite_foods"],
            favorite_menus=data["favorite_menus"],
        )

    def update_favorite_foods(self, user_id, favorites) -> Optional[Profile]:
        updated = self.profile_database.update_fields(
            user_id, {"favorite_foods": favorites}
        )
        if not updated:
            return None
        return Profile(
            user_id=int(updated["user_id"]),
            favorite_foods=updated["favorite_foods"],
            unfavorite_foods=updated["unfavorite_foods"],
            favorite_menus=updated["favorite_menus"],
        )

    # Favorite Menu Functions
    def add_favorite_menu(self, user_id: int, menu_id: str) -> bool:
        """Add a menu to user's favorites, check for duplicates beforehand
        Returns True if successful. False on failure."""
        profile_data = self.get_profile(user_id)
        if not profile_data:
            return False  # Can't add to non-existent profile

        favorite_menus = profile_data.favorite_menus
        favorite_menus.append(menu_id)
        profile_data.favorite_menus = favorite_menus

        return self.profile_database.update_profile(user_id, profile_data.to_dict())

    def remove_favorite_menu(self, user_id: int, menu_id: str) -> bool:
        """Remove a menu from user's favorites, check if it's there beforehand.
        Returns True if successful. False on failure."""
        profile_data = self.get_profile(user_id)
        # Duplicate check,
        # the one in the use case also happens to check for the user
        if not profile_data:
            return False  # Can't remove from non-existent profile

        favorite_menus = profile_data.favorite_menus
        if menu_id in favorite_menus:
            favorite_menus.remove(menu_id)

        profile_data.favorite_menus = favorite_menus
        return self.profile_database.update_profile(user_id, profile_data.to_dict())

    def get_favorite_menus(self, user_id: int) -> list:
        """Get all favorite menu IDs for a user"""
        profile_data = self.get_profile(user_id)
        if not profile_data:
            return []

        return profile_data.favorite_menus

    def is_menu_in_favorites(self, user_id: int, menu_id: str) -> bool:
        """Check if a menu is in user's favorites"""
        return menu_id in self.get_favorite_menus(user_id)

    def delete_profile(self, user_id: int) -> bool:
        """Delete a user's profile.
        Returns True if successful. False on failure."""
        return self.profile_database.delete_profile(user_id)

    def restore_profile(self, user_id: int, favorites: list) -> Optional[Profile]:
        profile_data = {
            "user_id": user_id,
            "favorite_foods": favorites,
            "unfavorite_foods": [],
            "favorite_menus": [],
        }
        restored_profile_data = self.profile_database.create_profile(profile_data)
        if restored_profile_data:
            return Profile(
                user_id=int(restored_profile_data["user_id"]),
                favorite_foods=(
                    restored_profile_data["favorite_foods"].split(";")
                    if restored_profile_data["favorite_foods"]
                    else []
                ),
                unfavorite_foods=(
                    restored_profile_data["unfavorite_foods"].split(";")
                    if restored_profile_data["unfavorite_foods"]
                    else []
                ),
                favorite_menus=(
                    restored_profile_data["favorite_menus"].split(";")
                    if restored_profile_data["favorite_menus"]
                    else []
                ),
            )
        return None
