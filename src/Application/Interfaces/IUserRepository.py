from abc import ABC, abstractmethod
from src.Application.DTOs.UserDTO import UserDTO
from src.Model.User.User import User

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
    def update_email(self, username: str, new_email: str):
        pass
    
    @abstractmethod
    def get_user_by_email(self, email):
        pass

    @abstractmethod
    def update_password_by_id(self, user_id: str, hashed_password: str):
        pass