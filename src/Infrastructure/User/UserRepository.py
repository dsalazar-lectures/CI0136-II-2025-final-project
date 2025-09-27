import json # For handling JSON data
from src.Model.User.User import User
from src.Database.User.UserSchema import UserSchema # Import the UserSchema for database
from src.Application.DTOs.UserDTO import UserDTO # Import the UserDTO for data transfer


class UserRepository():
    def __init__(self, db_connection): # Assumming db_connection
        self.user_schema = UserSchema(db_connection)

    def user_exists(self, username, email):
        # TODO: Check if user exists in the database
        return self.user_schema.user_exists(username, email) # Assuming user_schema has method user_exists

    def create_user(self, user_dto):
        # TODO: Create user in the database

        if self.user_exists(user_dto.username, user_dto.email):
            raise ValueError("User with this username or email already exists")

        # Convert DTO to JSON (dictionary)
        user_data = {
            "username": user_dto.username,
            "password": user_dto.password,
            "email": user_dto.email,
            "role": user_dto.role
        }

        created_user = self.user_schema.create_user(user_data) # Call create_user method from UserSchema

        if created_user:
            return User(
                id=created_user['id'],
                username=created_user['username'],
                email=created_user['email'],
                role=created_user['role']
            )
        return None

    def get_user_by_username(self, username):
        db_user = self.user_schema.get_user_by_username(username)

        if db_user:
            return User(
                id=db_user['id'],
                username=db_user['username'],
                email=db_user['email'],
                role=db_user['role']
            )
        return None
