from abc import ABC, abstractmethod
from typing import List, Optional
from src.Model.Profiles.Profiles import Profile

class IProfileRepository(ABC):
    @abstractmethod
    def create_profile(self, user_id):
        pass

    @abstractmethod
    def get_profile(self, user_id) -> Optional[Profile]:
        pass

    @abstractmethod
    def update_favorite_foods(self, user_id, favorites) -> Optional[Profile]:
        pass
