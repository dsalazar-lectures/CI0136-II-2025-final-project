from abc import ABC, abstractmethod


class IProfileApplicationService(ABC):

    @abstractmethod
    def create_profile(self, user_id: int):
        pass
