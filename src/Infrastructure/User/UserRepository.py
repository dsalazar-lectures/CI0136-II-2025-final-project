import json # For handling JSON data
from src.Model.User.User import User
from src.Database.User.UserSchema import UserSchema # Import the UserSchema for database
from src.Application.DTOs.UserDTO import UserDTO # Import the UserDTO for data transfer

class UserRepository():
    def __init__(self, database_connection): # Assumming db_connection
        self.user_schema = UserSchema(database_connection)

    def user_exists(self, username, email):
        # TODO: Check if user exists in the database
        return self.user_schema.user_exists(username, email) # Assuming user_schema has method user_exists

    def create_user(self, user_dto):
        # TODO: Create user in the database
        
        if self.user_exists(user_dto.username, user_dto.email):
            raise ValueError("User with this username or email already exists")


    def get_user_by_username(self, username):
        pass
