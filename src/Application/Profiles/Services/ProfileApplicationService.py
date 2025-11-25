from src.Application.Interfaces.IProfileApplicationService import (
    IProfileApplicationService,
)
from src.Model.Profiles.Profiles import Profile
from typing import List, Optional, Any


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

    def delete_profile(self, user_id):
        return self.profile_repository.delete_profile(user_id)

    def restore_profile(self, user_id: int, favorites: List[str]) -> Optional[Profile]:
        favorites_norm = [
            f.replace("-", " ").strip().lower() for f in favorites if isinstance(f, str)
        ]
        return self.profile_repository.restore_profile(user_id, favorites_norm)
    
    def set_unfavorite_ingredients(
        self, user_id: int, unfavorites: List[Any]
    ) -> Optional[Profile]:
        """ Update unfavorite_foods for the user. """

        ingredients_norm: List[str] = []

        for item in unfavorites:
            if isinstance(item, dict):
                ingredient_raw = item.get("ingredient")
            else:
                ingredient_raw = item

            if not isinstance(ingredient_raw, str):
                continue  # ignore non-string entries

            ingredient = ingredient_raw.replace("-", " ").strip().lower()
            if not ingredient:
                continue

            ingredients_norm.append(ingredient)

        return self.profile_repository.update_unfavorite_foods(
            user_id, ingredients_norm
        )
