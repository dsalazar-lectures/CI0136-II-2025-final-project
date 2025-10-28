from abc import ABC, abstractmethod
from typing import Optional
from src.Model.Profiles.Profiles import Profile

class IProfileRepository(ABC):
    @abstractmethod
    def create_profile(self, user_id):
        pass

    @abstractmethod
    def get_profile_by_user_id(self, user_id: str) -> Optional[dict]:
        """Return profile dict or None if not found"""
        pass

    # Favorite Menu Functions
    @abstractmethod
    def add_favorite_menu(self, user_id: str, menu_id: str) -> bool:
        """Add a menu to user's favorites, check for duplicates beforehand
        Returns True if successful. False on failure."""
        pass

    @abstractmethod
    def remove_favorite_menu(self, user_id: str, menu_id: str) -> bool:
        """Remove a menu from user's favorites, check if it's there beforehand.
        Returns True if successful. False on failure."""
        pass

    @abstractmethod
    def get_favorite_menus(self, user_id: str) -> list:
        """Get all favorite menu IDs for a user."""
        pass

    @abstractmethod
    def is_menu_in_favorites(self, user_id: str, menu_id: str) -> bool:
        """Check if a menu is in user's favorites."""
        pass
