from src.Model.User.User import User


class UserManager:
    def __init__(self):
        self.users = []
        self.next_id = 1

    def create_user(self, username, password, email, role="user"):
        for user in self.users:
            if user.username == username:
                return None, "Username already exists"
            if user.email == email:
                return None, "Email already exists"

        new_user = User(
            id=self.next_id,
            username=username,
            password=password,
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
