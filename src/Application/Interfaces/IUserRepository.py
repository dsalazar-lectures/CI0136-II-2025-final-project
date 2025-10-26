from abc import ABC, abstractmethod


class IUserRepository(ABC):
    @abstractmethod
    def user_exists(self, username, email):
        pass

    @abstractmethod
    def create_user(self, user_dto):
        pass

    @abstractmethod
    def get_user_by_username(self, username):
        pass

    @abstractmethod
    def create_user_profile(self, user_id: int):
        pass
