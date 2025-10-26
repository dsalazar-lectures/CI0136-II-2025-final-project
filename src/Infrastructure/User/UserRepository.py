from src.Application.Interfaces.IUserRepository import IUserRepository
from src.Model.User.User import User
from src.Application.DTOs.UserDTO import UserDTO
from src.Database.User.UserCSV import UserCSV

class UserRepository(IUserRepository):

    def __init__(self, csv_file_path="users.csv"):
        self.user_csv = UserCSV(csv_file_path)

    def user_exists(self, username, email):
        return self.user_csv.user_exists(username, email)

    def create_user(self, user_dto):
        if self.user_exists(user_dto.username, user_dto.email):
            return None, "User already exists", 400

        created_user_data = self.user_csv.create_user(user_dto)
        if created_user_data:
            user_entity = User(
                id=int(created_user_data['id']),
                username=created_user_data['username'],
                password=created_user_data['password'],
                email=created_user_data['email'],
                role=created_user_data['role']
            )
            return user_entity, "User created successfully", 201
        return None, "Failed to create user", 400

    def get_user_by_username(self, username):
        db_user = self.user_csv.get_user_by_username(username)
        if db_user:
            return UserDTO(
                id=int(db_user['id']),
                username=db_user['username'],
                password=db_user['password'],
                email=db_user['email'],
                role=db_user['role']
            )
        return None
    
    def update_password(self, username, hashed_password):
        updated = self.user_csv.update_password(username, hashed_password)
        if updated:
            return True, "Password updated successfully", 200
        return False, "Failed to update password", 400
    
    def update_email(self, username, new_email):
        updated = self.user_csv.update_email(username, new_email)
        if updated:
            return True, "Email updated successfully", 200
        return False, "Failed to update email", 400