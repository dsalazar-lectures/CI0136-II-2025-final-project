from src.Application.Interfaces.IProfileApplicationService import (
    IProfileApplicationService,
)


class MockProfileService(IProfileApplicationService):
    def __init__(self):
        self.created_profiles = []

    def create_profile(self, user_id: int):
        profile = {"user_id": user_id, "profile_id": len(self.created_profiles) + 1}
        self.created_profiles.append(profile)
        return profile

    def get_profile(self, user_id: int):
        profile = next(
            (p for p in self.created_profiles if p["user_id"] == user_id), None
        )
        return profile
