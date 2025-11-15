from abc import ABC, abstractmethod


class IProfileApplicationService(ABC):

    @abstractmethod
    def create_profile(self, user_id: int):
        pass

    @abstractmethod
    def get_profile(self, user_id: int):
        pass

    @abstractmethod
    def set_favorite_ingredients(self, user_id: int, favorites: list):
        pass

    @abstractmethod
    def delete_profile(self, user_id: int) -> bool:
        pass
