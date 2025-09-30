class UserDTO:
    def __init__(self, username, password, email, role="user"):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
    
    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'role': self.role
        }