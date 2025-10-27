from src.Application.Interfaces.IProfileApplicationService import (
    IProfileApplicationService,
)


class ProfileApplicationService(IProfileApplicationService):
    def __init__(self, profile_repository):
        self.profile_repository = profile_repository

    def create_profile(self, user_id: int):
        return self.profile_repository.create_profile(user_id)
