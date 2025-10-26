from abc import ABC, abstractmethod
from typing import List


class IProfileRepository(ABC):
    @abstractmethod
    def add_favorite_menu(self, user_id: str, menu_id: str) -> bool:
        """Add a menu to user's favorites. Returns True if successful."""
        pass

    @abstractmethod
    def remove_favorite_menu(self, user_id: str, menu_id: str) -> bool:
        """Remove a menu from user's favorites. Returns True if successful."""
        pass

    @abstractmethod
    def get_favorite_menus(self, user_id: str) -> List[str]:
        """Get all favorite menu IDs for a user."""
        pass

    @abstractmethod
    def is_menu_in_favorites(self, user_id: str, menu_id: str) -> bool:
        """Check if a menu is in user's favorites."""
        pass
