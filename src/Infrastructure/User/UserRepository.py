from src.Application.Interfaces.IUserRepository import IUserRepository
from src.Model.User.User import User
from src.Application.DTOs.UserDTO import UserDTO
from src.Application.DTOs.UserResponseDTO import UserResponseDTO
from src.Database.User.UserCSV import UserCSV


class UserRepository(IUserRepository):

    def __init__(self, csv_file_path="users.csv"):
        self.user_csv = UserCSV(csv_file_path)

    def user_exists(self, username, email):
        return self.user_csv.user_exists(username, email)

    def create_user(self, user_dto):
        if self.user_exists(user_dto.username, user_dto.email):
            return None, "User already exists", 400

        created_user = self.user_csv.create_user(user_dto)
        if created_user:
            user = User(
                id=int(created_user["id"]),
                username=created_user["username"],
                password=created_user["password"],
                email=created_user["email"],
                role=created_user["role"],
                key=created_user["key"],
            )
            return user, "User created successfully", 201

        return None, "Failed to create user", 400

    def get_user_by_username(self, username):
        db_user = self.user_csv.get_user_by_username(username)
        if db_user:
            return UserDTO(
                id=int(db_user["id"]),
                username=db_user["username"],
                password=db_user["password"],
                email=db_user["email"],
                role=db_user["role"],
                key=db_user["key"],
            )
        return None

    def get_user_by_email(self, email):
        db_user = self.user_csv.get_user_by_email(email)
        if db_user:
            return UserDTO(
                id=int(db_user["id"]),
                username=db_user["username"],
                password=db_user["password"],
                email=db_user["email"],
                role=db_user["role"],
                key=db_user["key"],
            )
        return None

    def get_user_by_id(self, user_id):
        db_user = self.user_csv.get_user_by_id(user_id)
        if db_user:
            return UserResponseDTO(
                id=int(db_user["id"]),
                username=db_user["username"],
                email=db_user["email"],
                role=db_user["role"],
            )
        return None

    def update_password(self, username, hashed_password):
        return self.user_csv.update_password(username, hashed_password)

    def update_password_by_id(self, user_id, hashed_password):
        return self.user_csv.update_password_by_id(user_id, hashed_password)

    def update_user_key(self, username, new_key) -> bool:
        return self.user_csv.update_user_key(username, new_key)

    def update_email(self, username, new_email):
        return self.user_csv.update_email(username, new_email)

    def delete_user(self, user_id: int) -> bool:
        return self.user_csv.delete_user(user_id)
