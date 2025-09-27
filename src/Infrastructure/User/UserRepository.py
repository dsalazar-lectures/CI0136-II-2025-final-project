import json # For handling JSON data
from src.Model.User.User import User
from src.Database.User.UserSchema import UserSchema # Import the UserSchema for database
from src.Application.DTOs.UserDTO import UserDTO # Import the UserDTO for data transfer

class UserRepository():

    def user_exists(self, username, email):
        # TODO: Check if user exists in the database
        pass

    def create_user(self, user_dto):
        # TODO: Create user in the database
        pass

    def get_user_by_username(self, username):
        pass
