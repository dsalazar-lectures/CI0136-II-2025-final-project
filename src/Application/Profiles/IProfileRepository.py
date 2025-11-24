from abc import ABC, abstractmethod
from typing import Optional
from src.Model.Profiles.Profiles import Profile


class IProfileRepository(ABC):
    @abstractmethod
    def create_profile(self, user_id):
        """Create a new profile for a user."""
        pass

    @abstractmethod
    def get_profile(self, user_id) -> Optional[Profile]:
        pass

    @abstractmethod
    def update_favorite_foods(self, user_id, favorites) -> Optional[Profile]:
        pass

    # Favorite Menu Functions
    @abstractmethod
    def add_favorite_menu(self, user_id: int, menu_id: str) -> bool:
        """Add a menu to user's favorites, check for duplicates beforehand
        Returns True if successful. False on failure."""
        pass

    @abstractmethod
    def remove_favorite_menu(self, user_id: int, menu_id: str) -> bool:
        """Remove a menu from user's favorites, check if it's there beforehand.
        Returns True if successful. False on failure."""
        pass

    @abstractmethod
    def get_favorite_menus(self, user_id: int) -> list:
        """Get all favorite menu IDs for a user."""
        pass

    @abstractmethod
    def is_menu_in_favorites(self, user_id: int, menu_id: str) -> bool:
        """Check if a menu is in user's favorites."""
        pass

    @abstractmethod
    def delete_profile(self, user_id: int) -> bool:
        """Delete a user's profile.
        Returns True if successful. False on failure."""
        pass

    @abstractmethod
    def restore_profile(self, user_id: int, favorites: list) -> Optional[Profile]:
        """Restore a user's profile with given favorite foods.
        Returns the restored Profile if successful, None on failure."""
        pass
