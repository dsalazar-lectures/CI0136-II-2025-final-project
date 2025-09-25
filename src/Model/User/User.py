class User:
    def __init__(self, id, username, password, email, role="user"):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def to_dict(self):
        # Turn user object into a dictionary
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'role': self.role
        }
