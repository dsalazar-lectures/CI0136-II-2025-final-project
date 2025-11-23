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
    def update_password(self, username: str, hashed_password: str):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def update_user_key(self, username, new_key) -> bool:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass
