from abc import ABC, abstractmethod


class IProfileRepository(ABC):
    @abstractmethod
    def create_profile(self, user_id):
        pass
