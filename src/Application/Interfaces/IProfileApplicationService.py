from abc import ABC, abstractmethod


class IProfileApplicationService(ABC):

    @abstractmethod
    def create_profile(self, user_id: int):
        pass

    @abstractmethod
    def get_profile(self, user_id: int):
        pass

    @abstractmethod
    def delete_profile(self, user_id: int) -> bool:
        pass
