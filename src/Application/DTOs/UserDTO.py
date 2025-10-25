class UserDTO:
    def __init__(self, id, username, password, email, role="user", key=None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.key = key
    
    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'role': self.role
        }