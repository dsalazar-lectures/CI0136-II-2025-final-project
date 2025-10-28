from src.Application.Profiles.IProfileRepository import IProfileRepository
from src.Model.Profiles.Profiles import Profile
from src.Database.Profiles.ProfileCSV import ProfileCSV
from typing import Optional


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
