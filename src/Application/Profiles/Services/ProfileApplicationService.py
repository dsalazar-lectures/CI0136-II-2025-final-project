from src.Infrastructure.Profiles.ProfileRepository import (
    ProfileRepository,
)


class ProfileApplicationService:
    def __init__(self):
        self.profile_repository = ProfileRepository()

    def create_profile(self, user_id: int):
        return self.profile_repository.create_profile(user_id)
