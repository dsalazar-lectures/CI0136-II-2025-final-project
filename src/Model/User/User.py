class User:
    def __init__(self, id, username, password_hash, email, role="user"):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.role = role

    def to_dict(self):
        # Turn user object into a dictionary
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }
