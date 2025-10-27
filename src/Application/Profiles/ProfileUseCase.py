from Application.Profiles.IProfileRepository import IProfileRepository
from typing import List


class ProfileUseCase:
    def __init__(self, profile_repository: IProfileRepository):
        self.profile_repository = profile_repository

    def add_favorite_menu(self, user_id: str, menu_id: str) -> bool:
        """Add a menu to user's favorites
        Returns True if added successfully, False if already exists or failed"""
        if self.profile_repository.is_menu_in_favorites(user_id, menu_id):
            return False  # Already in favorites

        return self.profile_repository.add_favorite_menu(user_id, menu_id)

    def remove_favorite_menu(self, user_id: str, menu_id: str) -> bool:
        """Remove a menu from user's favorites
        Returns True if removed successfully, False if not found or failed"""
        if not self.profile_repository.is_menu_in_favorites(user_id, menu_id):
            return False  # Not in favorites

        return self.profile_repository.remove_favorite_menu(user_id, menu_id)

    def get_favorite_menus(self, user_id: str) -> List[str]:
        """Get all favorite menu IDs for a user"""
        return self.profile_repository.get_favorite_menus(user_id)
