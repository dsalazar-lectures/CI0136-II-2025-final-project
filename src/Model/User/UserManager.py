from src.Model.User.User import User
from src.Application.User.UserAuthent import UserAuthent

user_authentication = UserAuthent()

class UserManager:
    def __init__(self):
        self.users = []
        self.next_id = 1

    def user_exists(self, username, email):
        for user in self.users:
            if user.username == username:
                return True, "Username already exists"
            if user.email == email:
                return True, "Email already exists"
        return False, None

    def validate_userdata(self, username, password, email):
        if not username or not isinstance(username, str):
            return False, "Username is required"
        if not password or not isinstance(password, str):
            return False, "Password is required"
        if not email or not isinstance(email, str):
            return False, "Email is required"
        if "@" not in email or "." not in email:
            return False, "Invalid email format"
        return True, None

    def create_user(self, username, password, email, role="user"):
        is_valid, valid_msg = self.validate_userdata(username, password, email)
        if not is_valid:
            return None, valid_msg

        exists, exists_msg = self.user_exists(username, email)
        if exists:
            return None, exists_msg

        pw_hash = user_authentication.hash_password(password)  # bcrypt con salt interno
        new_user = User(
            id=self.next_id,
            username=username,
            password_hash=pw_hash,
            email=email,
            role=role
        )

        self.users.append(new_user)
        self.next_id += 1
        return new_user, "User created successfully"

    def get_user_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None
