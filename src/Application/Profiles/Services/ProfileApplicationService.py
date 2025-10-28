from src.Application.Interfaces.IProfileApplicationService import (
    IProfileApplicationService,
)
from src.Model.Profiles.Profiles import Profile
from src.Application.Profiles.IProfileRepository import IProfileRepository
from typing import List, Optional


class ProfileApplicationService(IProfileApplicationService):
    def __init__(self, profile_repository):
        self.profile_repository = profile_repository

    def create_profile(self, user_id: int):
        return self.profile_repository.create_profile(user_id)

    def get_profile(self, user_id: int) -> Optional[Profile]:
        return self.profile_repository.get_profile(user_id)

    def set_favorite_ingredients(
        self, user_id: int, favorites: List[str]
    ) -> Optional[Profile]:
        favorites_norm = [
            f.replace("-", " ").strip().lower() for f in favorites if isinstance(f, str)
        ]
        return self.profile_repository.update_favorite_foods(user_id, favorites_norm)
