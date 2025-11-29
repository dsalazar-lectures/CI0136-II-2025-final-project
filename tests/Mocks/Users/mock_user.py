class MockUser:
    def __init__(
        self,
        id=None,
        username=None,
        password=None,
        email=None,
        role="user",
        key=None,
    ):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.key = key

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
        }
