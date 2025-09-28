from src.Model.User.User import User
from src.Application.DTOs.UserDTO import UserDTO # Import the UserDTO for data transfer
from src.Database.User.UserCSV import UserCSV # Import the UserCSV

class UserRepository():
    def __init__(self, csv_file_path="users.csv"):
        self.user_csv = UserCSV(csv_file_path)  # Delegate to UserCSV

    def user_exists(self, username, email):
        # TODO: Check if user exists in the database
        return self.user_csv.user_exists(username, email) # Delegate to UserCSV

    def create_user(self, user_dto):
        # TODO: Create user in the database

        if self.user_exists(user_dto.username, user_dto.email):
            return None, "User already exists"

        created_user_data = self.user_csv.create_user(user_dto)
        if created_user_data:
            user_entity = User(
                id=created_user_data['id'],
                username=created_user_data['username'],
                # password = created_user_data['password'],  # Password is already hashed in UserApplicationService
                email=created_user_data['email'],
                role=created_user_data['role']
            )
            return user_entity, "User created successfully"
        return None, "Failed to create user"

    def get_user_by_username(self, username):
        db_user = self.user_csv.get_user_by_username(username)

        if db_user:
            return UserDTO(
                id=db_user['id'],
                username=db_user['username'],
                email=db_user['email'],
                role=db_user['role']
            )
        return None
