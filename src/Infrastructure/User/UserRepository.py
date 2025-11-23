import csv
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

        created_user_data = self.user_csv.create_user(user_dto)
        if created_user_data:
            user_entity = User(
                id=int(created_user_data["id"]),
                username=created_user_data["username"],
                password=created_user_data["password"],
                email=created_user_data["email"],
                role=created_user_data["role"],
                key=created_user_data["key"],
            )
            return user_entity, "User created successfully", 201
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
        updated = self.user_csv.update_password(username, hashed_password)
        if updated:
            return True, "Password updated successfully", 200
        return False, "Failed to update password", 400

    def update_user_key(self, username, new_key) -> bool:
        return self.user_csv.update_user_key(username, new_key)

    def delete_user(self, user_id: int) -> bool:
        return self.user_csv.delete_user(user_id)

    #new methods added
    def update_email(self, username, new_email):
        updated = self.user_csv.update_email(username, new_email)
        if updated:
            return True, "Email updated successfully", 200
        return False, "Failed to update email", 400
    
    def get_user_by_email(self, email):
        with open(self.user_csv.file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['email'] == email:
                    return UserDTO(
                        id=int(row['id']),
                        username=row['username'],
                        password=row['password'],
                        email=row['email'],
                        role=row['role'],
                        key=row.get('key', ''),
                    )
        return None

    def update_password_by_id(self, user_id: str, hashed_password: str):
        updated = False
        rows = []
        
        with open(self.user_csv.file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == user_id:
                    row['password'] = hashed_password
                    updated = True
                rows.append(row)
        
        if updated:
            with open(self.user_csv.file_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['id', 'username', 'password', 'email', 'role', 'key'])
                writer.writeheader()
                writer.writerows(rows)
            return True, "Password updated successfully", 200
        
        return False, "User not found", 404