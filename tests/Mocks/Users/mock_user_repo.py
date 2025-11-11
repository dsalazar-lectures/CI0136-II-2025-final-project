from src.Application.Interfaces.IUserRepository import IUserRepository
from src.Application.DTOs.UserDTO import UserDTO
from tests.Mocks.Users.mock_user import MockUser


class MockUserRepository(IUserRepository):
    def __init__(self, users=None):
        self._users = users or []
        self._next_id = 1

    def user_exists(self, username, email):
        return any(
            user.username == username or user.email == email for user in self._users
        )

    def create_user(self, user_dto):
        if self.user_exists(user_dto.username, user_dto.email):
            return None, "User already exists", 400

        created_dto = UserDTO(
            id=self._next_id,
            username=user_dto.username,
            password=user_dto.password,
            email=user_dto.email,
            role=user_dto.role,
            key="mock_key",
            token=user_dto.token,
        )

        mock_user = MockUser(
            id=self._next_id,
            username=user_dto.username,
            password=user_dto.password,
            email=user_dto.email,
            role=user_dto.role,
            key="mock_key",
            token=user_dto.token,
        )
        self._users.append(mock_user)
        self._next_id += 1

        return created_dto, "User created successfully", 201

    def get_user_by_username(self, username):
        for user in self._users:
            if user.username == username:
                return user
        return None

    def get_user_by_id(self, user_id):
        for user in self._users:
            if user.id == user_id:
                return user
        return None

    def get_user_by_token(self, token):
        for user in self._users:
            if user.token == token:
                return user
        return None

    def update_user_token(self, username, token, key):
        for user in self._users:
            if user.username == username:
                user.token = token
        return False

    def update_password(self, username: str, hashed_password: str):
        for user in self._users:
            if user.username == username:
                user.password = hashed_password
                return True, "Password updated successfully", 200
        return False, "Failed to update password", 400
